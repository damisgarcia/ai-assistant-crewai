export default () => {
  function fetchAll(conversationId: string) {
    const options = useFetchApiOptions();
    return $fetch<any[]>(`conversation/${conversationId}/message/`, options);
  }

  function create(conversationId: string, data: { content: string }) {
    const options = useFetchApiOptions({
      method: "POST",
      body: {
        conversation: +conversationId,
        sender_type: "user",
        content: data.content,
      },
    });

    return $fetch<any[]>(`conversation/${conversationId}/message/`, options);
  }

  return {
    fetchAll,
    create,
  };
};
