#!/bin/bash

# Generate TypeScript code from proto files
npx pbjs -t static-module -w commonjs -o karna-react-frontend/src/generated/messages.js proto/messages.proto
npx pbts -o karna-react-frontend/src/generated/messages.d.ts karna-react-frontend/src/generated/messages.js