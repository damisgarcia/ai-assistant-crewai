import { useWebSocket, createEventHook } from "@vueuse/core";

const provideKey = "trend";

function composable() {
  const maxRetries = 3;
  const retryDelay = 1000; // milliseconds
  const retryCount = shallowRef(0);

  const client = shallowRef<{
    send: (data: string | ArrayBuffer | Blob) => void;
    status: Ref<"CONNECTING" | "OPEN" | "CLOSING" | "CLOSED">;
    ws: Ref<WebSocket | undefined>;
  } | null>(null);

  const conversationId = ref<string | null>(null);

  const connectHook = createEventHook();
  const disconnectHook = createEventHook();
  const messageHook = createEventHook<any>();

  const ws = computed(() => client.value?.ws.value);
  const ws_status = computed(() => client.value?.status.value);

  watch(conversationId, (newId, oldId) => {
    if (newId != oldId) {
      retryCount.value = 0; // Reset retry count when conversation changes
    }
  });

  function connect(trendId: string) {
    conversationId.value = trendId;

    if (retryCount.value > maxRetries) {
      throw new Error("Max retries reached. Unable to connect to WebSocket.");
    }

    if (ws_status.value && ws_status.value !== "CLOSED") {
      retryCount.value++;
      return setTimeout(() => connect(trendId), retryDelay);
    }

    const { send, status, ws } = useWebSocket(
      `${import.meta.env.VITE_WS_BASE_URL}/trend/${trendId}/`,
      {
        onError: (error) => {
          console.error("WebSocket error:", error);
        },
      }
    );

    client.value = { send, status, ws };
    retryCount.value = 0;

    bindEvents();
  }

  function disconnect() {
    ws.value?.close();
    unbindEvents();
  }

  function bindEvents() {
    if (ws.value) {
      ws.value?.addEventListener("open", onOpen);
      ws.value?.addEventListener("close", onClose);
      ws.value?.addEventListener("message", handleMessage);
    }
  }

  function unbindEvents() {
    if (ws.value) {
      ws.value?.removeEventListener("open", onOpen);
      ws.value?.removeEventListener("close", onClose);
      ws.value?.removeEventListener("message", handleMessage);
    }
  }

  function onOpen() {
    connectHook.trigger();
  }

  function onClose() {
    disconnectHook.trigger();
  }

  function handleMessage(event: MessageEvent) {
    const data = JSON.parse(event.data);
    messageHook.trigger(data);
  }

  function sendMessage(data: string) {
    if (client.value) {
      client.value.send(
        JSON.stringify({
          type: "message",
          conversation_id: conversationId.value,
          content: data,
        })
      );
    } else {
      console.warn("WebSocket client is not connected");
    }
  }

  return {
    client,
    connect,
    disconnect,
    sendMessage,
    onConnected: connectHook.on,
    onDisconnected: disconnectHook.on,
    onMessage: messageHook.on,
    status: ws_status,
  };
}

export function provideTrend() {
  const trend = composable();
  return provide(provideKey, trend);
}

export function useTrend() {
  const trend = inject(provideKey);

  if (!trend) {
    throw new Error("useTrend must be used within a provideTrend context");
  }

  return trend as ReturnType<typeof composable>;
}
