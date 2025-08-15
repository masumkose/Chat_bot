// app/assistant.tsx
"use client";

import { AssistantRuntimeProvider } from "@assistant-ui/react";
import { useChatRuntime } from "@assistant-ui/react-ai-sdk";
import { Thread } from "@/components/assistant-ui/thread";

// Bu, gömülü (embedded) kullanım için sadeleştirilmiş versiyondur.
// Artık tam sayfa düzenini (header, sidebar vb.) içermiyor.
export const Assistant = () => {
  const runtime = useChatRuntime({
    api: "/api/chat",
  });

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      {/*
        Bu sarmalayıcı div, bileşenin kendisine verilen alana tam olarak
        yayılmasını ve sohbet akışının düzgün çalışmasını sağlar.
      */}
      <div className="relative flex h-full flex-col">
        {/* Thread bileşeni, mesajları ve giriş alanını içerir */}
        <Thread />
      </div>
    </AssistantRuntimeProvider>
  );
};