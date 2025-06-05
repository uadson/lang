import { ref } from "vue";

export function useTranslator() {
  const sourceText = ref("");
  const translatedText = ref("");
  const sourceLanguage = ref("pt");
  const targetLanguage = ref("en");
  const isTranslating = ref(false);

  const translateText = async () => {
    if (!sourceText.value.trim()) return;

    isTranslating.value = true;

    // Simulação de tradução (em um app real, você usaria uma API de tradução)
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // Traduções simuladas simples
    const translations = {
      "pt-en": {
        olá: "hello",
        mundo: "world",
        "bom dia": "good morning",
        obrigado: "thank you",
        "como você está?": "how are you?",
      },
      "en-pt": {
        hello: "olá",
        world: "mundo",
        "good morning": "bom dia",
        "thank you": "obrigado",
        "how are you?": "como você está?",
      },
    };

    const key = `${sourceLanguage.value}-${targetLanguage.value}`;
    const lowerText = sourceText.value.toLowerCase();

    translatedText.value =
      translations[key]?.[lowerText] ||
      `[Tradução simulada] ${sourceText.value}`;

    isTranslating.value = false;
  };

  const swapLanguages = () => {
    const temp = sourceLanguage.value;
    sourceLanguage.value = targetLanguage.value;
    targetLanguage.value = temp;

    const tempText = sourceText.value;
    sourceText.value = translatedText.value;
    translatedText.value = tempText;
  };

  const clearText = () => {
    sourceText.value = "";
    translatedText.value = "";
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      // Feedback visual poderia ser adicionado aqui
    });
  };

  return {
    sourceText,
    translatedText,
    sourceLanguage,
    targetLanguage,
    isTranslating,
    translateText,
    swapLanguages,
    clearText,
    copyToClipboard,
  };
}
