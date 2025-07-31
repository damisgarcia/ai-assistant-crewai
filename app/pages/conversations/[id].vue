<script lang="ts" setup>
import { triggerRef } from "vue";

const route = useRoute();
const messageStore = useMessageStore();
const { pendingMessage } = storeToRefs(messageStore);
const Conversation = useConversation();
const Message = useConversationMessage();
const Trend = useTrend();

const message = ref("");
const typing = ref(false);
const messageContainer = useTemplateRef("message-container");

await useAsyncData(`conversation:${route.params.id}`, async () => {
  const id = route.params.id as string;
  return await Conversation.fetchOne(id);
});

const { data: messages, pending } = await useAsyncData(
  `conversation:${route.params.id}:messages`,
  async () => {
    const id = route.params.id as string;
    return await Message.fetchAll(id);
  }
);

onMounted(() => {
  Trend.connect(route.params.id as string);

  Trend.onConnected(() => {
    console.log("Trend connected", pendingMessage.value);
    if (pendingMessage.value.length > 0) {
      Trend.sendMessage(pendingMessage.value);
      messageStore.clearPendingMessage();
    }
  });

  Trend.onMessage((data) => {
    if (data.type === "message") {
      if (Array.isArray(messages.value)) {
        messages.value.push(data.message);
        triggerRef(messages); // Força o Vue a re-renderizar por conta do AsyncData
      }

      setTimeout(() => {
        messageContainer.value?.scrollToMessage();
      }, 600);
    }

    typing.value = data.type === "typing";
  });
});

onUnmounted(() => {
  Trend.disconnect();
});

async function onMessage() {
  Trend.sendMessage(message.value);
}
</script>

<template>
  <layout-content class="relative col-span-4">
    <loader-message :visible="pending" />
    <conversation-message-container ref="message-container">
      <conversation-message v-for="m in messages" :key="m.id" :message="m" />
    </conversation-message-container>
    <div v-if="typing" class="max-w-screen-2xl mx-auto">
      <div class="rounded-full bg-blue-200/20 px-4 py-2 bottom-2 right-2 w-fit">
        Aguarde alguns instantes...
      </div>
    </div>
    <ConversationInput v-model="message" :typing="typing" @submit="onMessage" />
  </layout-content>
</template>
