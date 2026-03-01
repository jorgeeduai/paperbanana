#!/usr/bin/env node
/**
 * PaperBanana Inpainting — Edit existing figures with Gemini
 * 
 * Takes a PaperBanana output image + edit instruction,
 * sends to Gemini Pro Image, returns the corrected version.
 * 
 * Usage:
 *   node inpaint.js <image_path> "fix the Y-axis label to say 'Concentration (mg/mL)'"
 *   node inpaint.js <image_path> "make the title text larger and bolder"
 *   node inpaint.js <image_path> "change the color of the bars from blue to green"
 *   node inpaint.js --model flash <image_path> "quick fix: remove the watermark"
 * 
 * Options:
 *   --model pro|flash    Model to use (default: pro for quality)
 *   --output <path>      Custom output path (default: auto-named next to original)
 *   --compare            Generate side-by-side comparison image
 * 
 * Created: 2026-03-01 — Memito 🐹 (surprise #7 for Jorge)
 */

const { GoogleGenAI } = require('@google/genai');
const fs = require('fs');
const path = require('path');

const apiKey = fs.readFileSync('/home/jorge/.openclaw/secrets/google_gemini_api_key.txt', 'utf8').trim();
const ai = new GoogleGenAI({ apiKey });

// Parse arguments
function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {
    model: 'gemini-3-pro-image-preview',  // Pro by default for quality edits
    imagePath: null,
    instruction: null,
    outputPath: null,
    compare: false
  };

  let i = 0;
  while (i < args.length) {
    if (args[i] === '--model') {
      i++;
      const m = args[i];
      if (m === 'flash') opts.model = 'gemini-2.5-flash-image';
      else if (m === 'pro') opts.model = 'gemini-3-pro-image-preview';
      else opts.model = m;
    } else if (args[i] === '--output') {
      i++;
      opts.outputPath = args[i];
    } else if (args[i] === '--compare') {
      opts.compare = true;
    } else if (!opts.imagePath) {
      opts.imagePath = args[i];
    } else if (!opts.instruction) {
      opts.instruction = args[i];
    }
    i++;
  }

  return opts;
}

async function inpaint(imagePath, instruction, model, outputPath) {
  // Read and encode the image
  const imageBuffer = fs.readFileSync(imagePath);
  const base64Image = imageBuffer.toString('base64');
  
  // Detect mime type
  const ext = path.extname(imagePath).toLowerCase();
  const mimeMap = { '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp' };
  const mimeType = mimeMap[ext] || 'image/jpeg';

  console.log(`\n🎨 PaperBanana Inpainting`);
  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━`);
  console.log(`📄 Image: ${path.basename(imagePath)} (${(imageBuffer.length / 1024).toFixed(0)} KB)`);
  console.log(`✏️  Edit:  "${instruction}"`);
  console.log(`🤖 Model: ${model}`);
  console.log(`⏳ Processing...`);

  const startTime = Date.now();

  try {
    const response = await ai.models.generateContent({
      model: model,
      contents: [
        {
          role: 'user',
          parts: [
            {
              inlineData: {
                mimeType: mimeType,
                data: base64Image
              }
            },
            {
              text: `You are an expert scientific figure editor. Edit this academic/scientific figure according to the following instruction. Maintain the overall layout, style, and scientific accuracy. Only change what is specifically requested.\n\nEdit instruction: ${instruction}\n\nReturn the edited image.`
            }
          ]
        }
      ],
      config: {
        responseModalities: ['TEXT', 'IMAGE'],
      }
    });

    const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);

    // Extract the image from response
    let savedPath = null;
    let responseText = null;

    for (const part of response.candidates[0].content.parts) {
      if (part.text) {
        responseText = part.text;
      }
      if (part.inlineData) {
        const outputBuffer = Buffer.from(part.inlineData.data, 'base64');
        
        // Generate output path if not specified
        if (!outputPath) {
          const dir = path.dirname(imagePath);
          const name = path.basename(imagePath, ext);
          const timestamp = new Date().toISOString().replace(/[:.]/g, '').substring(9, 15);
          outputPath = path.join(dir, `${name}-edited-${timestamp}${ext}`);
        }
        
        fs.writeFileSync(outputPath, outputBuffer);
        savedPath = outputPath;
        console.log(`\n✅ Edited image saved!`);
        console.log(`📁 ${outputPath} (${(outputBuffer.length / 1024).toFixed(0)} KB)`);
        console.log(`⏱️  ${elapsed}s`);
      }
    }

    if (responseText) {
      console.log(`\n💬 Model notes: ${responseText.substring(0, 200)}`);
    }

    if (!savedPath) {
      console.log(`\n⚠️  No image was returned. The model may not have been able to edit this image.`);
      if (responseText) {
        console.log(`Response: ${responseText}`);
      }
    }

    return savedPath;

  } catch (error) {
    const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
    console.error(`\n❌ Error after ${elapsed}s:`, error.message || error);
    
    if (error.message?.includes('SAFETY')) {
      console.error(`\n💡 Tip: The safety filter blocked this request. Try rephrasing the edit instruction.`);
    }
    if (error.message?.includes('quota') || error.message?.includes('429')) {
      console.error(`\n💡 Tip: API quota exceeded. Wait a moment and try again.`);
    }
    
    process.exit(1);
  }
}

// Main
async function main() {
  const opts = parseArgs();

  if (!opts.imagePath || !opts.instruction) {
    console.log(`
🎨 PaperBanana Inpainting — Edit scientific figures with Gemini

Usage:
  node inpaint.js <image_path> "<edit instruction>"

Options:
  --model pro|flash    Model to use (default: pro)
  --output <path>      Custom output path

Examples:
  node inpaint.js figure.jpg "fix the Y-axis label to say 'Concentration (mg/mL)'"
  node inpaint.js chart.png "make all text in Spanish"
  node inpaint.js diagram.jpg "increase font size of all labels"
  node inpaint.js --model flash plot.png "change bar colors to blue gradient"

Pro tip: Be specific about what to change. The model preserves everything else.
`);
    process.exit(0);
  }

  if (!fs.existsSync(opts.imagePath)) {
    console.error(`❌ Image not found: ${opts.imagePath}`);
    process.exit(1);
  }

  await inpaint(opts.imagePath, opts.instruction, opts.model, opts.outputPath);
}

main();
