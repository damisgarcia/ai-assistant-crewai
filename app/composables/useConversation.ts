export default () => {
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

  return {
    fetchAll,
    create,
  };
};
