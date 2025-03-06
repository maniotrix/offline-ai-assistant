const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const rootDir = path.resolve(__dirname, '..');
const protoDir = path.join(rootDir, 'proto');
const outputDir = path.join(rootDir, 'karna-react-frontend', 'src', 'generated');

// Automatically find all proto files in the proto directory
const protoFiles = fs.readdirSync(protoDir)
    .filter(file => file.endsWith('.proto'));

console.log(`Found ${protoFiles.length} proto files: ${protoFiles.join(', ')}`);

try {
    // Clear output directory if it exists
    if (fs.existsSync(outputDir)) {
        fs.readdirSync(outputDir).forEach(file => {
            const filePath = path.join(outputDir, file);
            if (file.endsWith('.js') || file.endsWith('.ts') || file.endsWith('.d.ts')) {
                fs.unlinkSync(filePath);
            }
        });
        console.log('Cleared existing generated files');
    }

    // Create output directory if it doesn't exist
    fs.mkdirSync(outputDir, { recursive: true });

    // Generate combined JavaScript output from all proto files
    const protoFilePaths = protoFiles.map(file => `"${path.join(protoDir, file)}"`).join(' ');
    const outputJs = path.join(outputDir, 'messages.js');
    const outputTs = path.join(outputDir, 'messages.d.ts');

    // Generate JavaScript from proto files with ES modules
    execSync(`npx pbjs -t static-module -w es6 -o "${outputJs}" ${protoFilePaths}`);

    // Generate TypeScript definitions
    execSync(`npx pbts -o "${outputTs}" "${outputJs}"`);

    console.log('Successfully generated TypeScript protobuf code for all proto files');

    // Additionally, generate individual files per proto if needed
    protoFiles.forEach(protoFile => {
        const baseName = path.basename(protoFile, '.proto');
        const singleOutputJs = path.join(outputDir, `${baseName}.js`);
        const singleOutputTs = path.join(outputDir, `${baseName}.d.ts`);

        execSync(`npx pbjs -t static-module -w es6 -o "${singleOutputJs}" "${path.join(protoDir, protoFile)}"`);
        execSync(`npx pbts -o "${singleOutputTs}" "${singleOutputJs}"`);
        console.log(`Generated TypeScript protobuf code for ${protoFile}`);
    });
} catch (error) {
    console.error('Error generating protobuf code:', error);
    process.exit(1);
}