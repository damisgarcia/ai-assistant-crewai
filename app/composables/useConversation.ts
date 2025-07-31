export default () => {
  function fetchOne(id: string) {
    const options = useFetchApiOptions();
    return $fetch<any>(`conversation/${id}`, options);
  }

  function fetchAll() {
    const options = useFetchApiOptions();
    return $fetch<any[]>("conversation", options);
  }

  function create(data: { title: string }) {
    const options = useFetchApiOptions({
      method: "POST",
      body: data,
    });

    return $fetch<any>("conversation/", options);
  }

  function destroy(id: string) {
    const options = useFetchApiOptions({
      method: "DELETE",
    });

    return $fetch<any>(`conversation/${id}/`, options);
  }

  return {
    destroy,
    fetchOne,
    fetchAll,
    create,
  };
};
