type useMessageStore = ReturnType<typeof useMessageStore>;

export const useMessageStore = defineStore("message", () => {
  const pendingMessage = ref("");

  function setPendingMessage(message: string) {
    pendingMessage.value = message;
  }

  function clearPendingMessage() {
    pendingMessage.value = "";
  }

  return {
    pendingMessage,
    setPendingMessage,
    clearPendingMessage,
  };
});
