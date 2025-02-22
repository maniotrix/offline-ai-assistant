const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const rootDir = path.resolve(__dirname, '..');
const protoFile = path.join(rootDir, 'proto', 'messages.proto');
const outputDir = path.join(rootDir, 'karna-react-frontend', 'src', 'generated');
const outputJs = path.join(outputDir, 'messages.js');
const outputTs = path.join(outputDir, 'messages.d.ts');

try {
    // Create output directory if it doesn't exist
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }

    // Generate JavaScript from proto with ES modules
    execSync(`npx pbjs -t static-module -w es6 -o "${outputJs}" "${protoFile}"`);

    // Generate TypeScript definitions
    execSync(`npx pbts -o "${outputTs}" "${outputJs}"`);

    console.log('Successfully generated TypeScript protobuf code');
} catch (error) {
    console.error('Error generating protobuf code:', error);
    process.exit(1);
}