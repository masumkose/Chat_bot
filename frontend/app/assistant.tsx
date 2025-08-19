// frontend/app/assistant.tsx
"use client";

import { AssistantRuntimeProvider, useAssistantRuntime } from "@assistant-ui/react";
import { useChatRuntime } from "@assistant-ui/react-ai-sdk";
import { Thread } from "@/components/assistant-ui/thread";
import { useEffect, useState } from "react";

// A custom hook to manage the backend wake-up sequence
const useBackendWakeUp = () => {
  const runtime = useAssistantRuntime();
  const [hasWakeUpAttempted, setHasWakeUpAttempted] = useState(false);

  useEffect(() => {
    // Only run this effect once, and only if the runtime is ready.
    if (!runtime || hasWakeUpAttempted) {
      return;
    }

    // Mark that we are attempting to wake up the backend.
    setHasWakeUpAttempted(true);

    const wakeUpBackend = async () => {
      // 1. Define a temporary "waking up" message with a unique ID.
      const wakingMessage = {
        id: "system-waking-up",
        role: "assistant" as const,
        content: [{ type: "text" as const, text: "Waking up the AI assistant... this may take a moment." }],
      };
      runtime.thread.addMessage(wakingMessage);

      try {
        // 2. Call the new /health endpoint. The time this fetch takes IS the cold start time.
        // We use a specific environment variable for the health check URL.
        const healthUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
        if (!healthUrl) {
          throw new Error("Backend URL is not configured.");
        }
        
        await fetch(`${healthUrl}/health`);

        // 3. If successful, remove the "waking up" message.
        // The user can now start chatting with a warm backend.
        runtime.thread.setMessages(messages =>
          messages.filter(m => m.id !== wakingMessage.id)
        );

      } catch (error) {
        console.error("Backend wake-up failed:", error);
        // 4. If it fails, replace the "waking up" message with an error.
        const errorMessage = {
            id: "system-error",
            role: "assistant" as const,
            content: [{ type: "text" as const, text: "Sorry, I couldn't connect to the AI assistant. Please try refreshing the page." }],
        };
        runtime.thread.setMessages(messages =>
            messages.filter(m => m.id !== wakingMessage.id).concat(errorMessage)
        );
      }
    };

    wakeUpBackend();
  }, [runtime, hasWakeUpAttempted]);
};


export const Assistant = () => {
  const runtime = useChatRuntime({
    api: "/api/chat",
  });

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <WakeUpManager />
      <div className="relative flex h-full flex-col">
        <Thread />
      </div>
    </AssistantRuntimeProvider>
  );
};

// This is a "headless" component that just runs our hook.
const WakeUpManager = () => {
  useBackendWakeUp();
  return null;
};
