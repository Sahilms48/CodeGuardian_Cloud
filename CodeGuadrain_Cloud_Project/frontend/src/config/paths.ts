import path from 'node:path';
import { fileURLToPath } from 'url';

// Get the current file's directory
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Define relative paths
export const PATHS = {
  finalReport: path.join(__dirname, '../../../final_report.md'),
  reportsDir: path.join(__dirname, '../../../reports')
} as const;
