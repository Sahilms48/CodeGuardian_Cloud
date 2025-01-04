import fs from 'node:fs';
import path from 'node:path';
import { PATHS } from '../config/paths';

export async function getMarkdownContent(filePath: string): Promise<string | null> {
  try {
    const content = await fs.promises.readFile(filePath, 'utf-8');
    return content;
  } catch (error) {
    return null;
  }
}

export async function getReportFiles(): Promise<string[]> {
  try {
    const files = await fs.promises.readdir(PATHS.reportsDir);
    return files
      .filter(file => file.toLowerCase().endsWith('.md'))
      .map(file => path.join(PATHS.reportsDir, file));
  } catch (error) {
    return [];
  }
}