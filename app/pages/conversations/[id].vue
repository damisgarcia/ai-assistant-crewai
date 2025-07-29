<script lang="ts" setup>
const route = useRoute();
const Conversation = useConversation();
const Message = useConversationMessage();
const Trend = useTrend();

const message = ref("");

await useAsyncData(`conversation:${route.params.id}`, async () => {
  const id = route.params.id as string;
  return await Conversation.fetchOne(id);
});

const {
  data: messages,
  refresh,
  pending,
} = await useAsyncData(
  `conversation:${route.params.id}:messages`,
  async () => {
    const id = route.params.id as string;
    return await Message.fetchAll(id);
  },
  { lazy: true, server: false }
);

onMounted(() => {
  Trend.connect(route.params.id as string);

  Trend.onConnected(() => {
    console.log("WebSocket connected for conversation:", route.params.id);
  });

  Trend.onMessage((data) => {
    console.log("Received message:", data);
  });
});

onUnmounted(() => {
  Trend.disconnect();
});

async function onMessage() {
  const id = route.params.id as string;

  Trend.sendMessage(message.value);

  await Message.create(id, {
    content: message.value,
  });

  refresh();
}
</script>

<template>
  <layout-content class="relative col-span-4">
    <loader-message :visible="pending" />
    <conversation-message-container>
      <lazy-conversation-message
        v-for="m in messages"
        :key="m.id"
        :message="m"
      />
    </conversation-message-container>
    <ConversationInput v-model="message" @submit="onMessage" />
  </layout-content>
</template>
