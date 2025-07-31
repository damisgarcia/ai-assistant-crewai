<script setup lang="ts">
const ask = defineModel({
  default: "",
  type: String,
});

const props = defineProps<{
  typing?: boolean;
}>();

const input = useTemplateRef("conversation-input");
const emit = defineEmits(["submit"]);

const sendIcon = computed(() => {
  return props.typing ? "zondicons:loading" : "zondicons:send";
});

function handleAsk() {
  if (props.typing) {
    return;
  }

  if (ask.value.trim()) {
    emit("submit", ask.value);

    ask.value = "";

    // Move o cursor para o início do textarea
    nextTick(() => {
      const textarea = input.value?.textareaRef as
        | HTMLTextAreaElement
        | undefined;

      if (textarea) {
        textarea.selectionStart = 0;
        textarea.selectionEnd = 0;
        textarea.focus();
      }
    });
  }
}
</script>

<template>
  <div class="w-full relative max-w-5xl mx-auto">
    <form @submit.prevent="handleAsk">
      <UTextarea
        ref="conversation-input"
        v-model="ask"
        highlight
        color="primary"
        placeholder="Pergunte alguma coisa"
        class="w-full"
        :autoresize="true"
        :autofocus="true"
        :rows="5"
        :disabled="props.typing"
        @keyup.prevent.enter="handleAsk"
      />
      <UButton
        v-if="!props.typing"
        icon="zondicons:send"
        size="md"
        color="primary"
        variant="ghost"
        type="submit"
        class="absolute rounded-full p-3 bottom-2 right-2"
        @click="handleAsk"
      />
    </form>
  </div>
</template>
