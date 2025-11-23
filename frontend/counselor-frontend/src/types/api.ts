/**
 * Standard API Response Format
 * Use this interface for all API route responses
 */
export interface ApiResponse<T = unknown> {
  data?: T;
  success: boolean;
  status: number;
  error?: string;
}

/**
 * Helper function to create success responses
 */
export function createSuccessResponse<T>(
  data: T,
  status: number = 200
): ApiResponse<T> {
  return {
    data,
    success: true,
    status,
  };
}

/**
 * Helper function to create error responses
 */
export function createErrorResponse(
  error: string,
  status: number = 400
): ApiResponse {
  return {
    success: false,
    status,
    error,
  };
}
