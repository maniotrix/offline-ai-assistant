import { SERVER_HOSTNAME, SERVER_PORT } from '../api/constants';

/**
 * Gets the full URL for an annotation image path
 */
export const getAnnotationImageUrl = (annotationPath: string | null | undefined): string => {
    if (!annotationPath) return '';
    
    // Ensure path starts with a forward slash
    const normalizedPath = annotationPath.startsWith('/') ? annotationPath : `/${annotationPath}`;
    
    return `http://${SERVER_HOSTNAME}:${SERVER_PORT}${normalizedPath}`;
};