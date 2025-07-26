export function useFetchApiOptions(options: any = {}) {
  const defaultOptions = {
    baseURL: import.meta.env.VITE_API_BASE_URL,
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json",
    },
  }

  return {
    ...defaultOptions,
    ...options,
  }
}