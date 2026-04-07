/**
 * Utility to get the correct path for an asset, taking into account the
 * base URL of the application (useful for GitHub Pages).
 */
export const getAssetPath = (path: string): string => {
  // Ensure the path doesn't start with a leading slash if we're prepending the base URL
  const cleanPath = path.startsWith('/') ? path.substring(1) : path;
  const baseUrl = import.meta.env.BASE_URL;
  
  // baseUrl already ends with a slash because it's '/LOOP_DEMO_OPENSC/'
  return `${baseUrl}${cleanPath}`;
};
