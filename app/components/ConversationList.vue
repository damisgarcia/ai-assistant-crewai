<script lang="ts" setup>
defineProps({
  conversations: {
    type: Array as () => { id: string; title: string }[],
    required: true,
  },
});

const route = useRoute();
const Conversation = useConversation();
const emit = defineEmits(["destroy"]);

async function destroy(id: string) {
  await Conversation.destroy(id);

  if (route.params.id == id) {
    navigateTo("/");
  }

  emit("destroy", id);
}
</script>

<template>
  <div>
    <div class="text-lg font-medium mb-6">Chats</div>
    <div class="flex flex-col gap-4">
      <div class="mb-4">
        <UButton
          size="lg"
          color="primary"
          variant="outline"
          as="router-link"
          to="/"
          icon="ic:twotone-article"
        >
          New Chat
        </UButton>
      </div>
      <div v-for="c in conversations" :key="c.id">
        <div class="conversation-item flex justify-stretch gap-2 group">
          <UButton
            size="lg"
            color="neutral"
            variant="ghost"
            as="router-link"
            :to="{ name: 'conversations-id', params: { id: c.id } }"
            class="w-fit"
            active-class="bg-gray-200 dark:bg-gray-700"
          >
            <span>
              {{ c.title }}
            </span>
          </UButton>
          <UPopover
            :content="{ side: 'right', align: 'start' }"
            :portal="false"
          >
            <UButton
              size="lg"
              color="neutral"
              variant="ghost"
              icon="qlementine-icons:menu-dots-16"
              class="p-1 text-3xl opacity-0 group-hover:opacity-100"
            />
            <template #content>
              <UButtonGroup>
                <UButton
                  size="sm"
                  color="neutral"
                  variant="ghost"
                  icon="ic:round-delete"
                  @click="destroy(c.id)"
                >
                  Delete
                </UButton>
              </UButtonGroup>
            </template>
          </UPopover>
        </div>
      </div>
    </div>
  </div>
</template>
