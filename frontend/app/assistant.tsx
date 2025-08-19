// frontend/app/assistant.tsx
"use client";

import { AssistantRuntimeProvider } from "@assistant-ui/react";
import { useChatRuntime } from "@assistant-ui/react-ai-sdk";
import { Thread, type VercelMessage } from "@/components/assistant-ui/thread"; // Import VercelMessage type
import { useEffect, useState } from "react";

// Define the type for our system message state
type SystemMessage = VercelMessage | null;

export const Assistant = () => {
  const [systemMessage, setSystemMessage] = useState<SystemMessage>(null);
  const [isBackendWakingUp, setIsBackendWakingUp] = useState(true);

  // This effect runs once on component mount to wake up the backend
  useEffect(() => {
    // Set the initial "waking up" message
    setSystemMessage({
      id: "system-waking-up",
      role: "assistant",
      content: "Waking up the AI assistant... this may take a moment.",
    });

    const wakeUpBackend = async () => {
      try {
        const healthUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
        if (!healthUrl) {
          throw new Error("Backend URL is not configured.");
        }
        
        // Call the /health endpoint. The time this fetch takes IS the cold start time.
        await fetch(`${healthUrl}/health`);

        // If successful, clear the system message and mark backend as ready.
        setSystemMessage(null);
        setIsBackendWakingUp(false);

      } catch (error) {
        console.error("Backend wake-up failed:", error);
        // If it fails, replace the message with an error.
        setSystemMessage({
            id: "system-error",
            role: "assistant",
            content: "Sorry, I couldn't connect to the AI assistant. Please try refreshing the page.",
        });
      }
    };

    wakeUpBackend();
  }, []); // Empty dependency array ensures this runs only once

  const runtime = useChatRuntime({
    api: "/api/chat",
    // Conditionally provide the initial messages
    initialMessages: systemMessage ? [systemMessage] : [],
  });
  
  // This effect will sync our local systemMessage with the runtime's state
  useEffect(() => {
    if (systemMessage) {
      // If our system message exists, make sure it's the only message in the thread
      runtime.thread.setMessages([systemMessage]);
    } else if (isBackendWakingUp === false && runtime.thread.messages.some(m => m.id === 'system-waking-up')) {
      // If backend is awake and the waking message is still there, clear it
      runtime.thread.setMessages([]);
    }
  }, [systemMessage, isBackendWakingUp, runtime.thread]);

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <div className="relative flex h-full flex-col">
        {/* We pass the disabled prop to the Thread's composer to prevent user input while waking up */}
        <Thread composerProps={{ disabled: isBackendWakingUp }} />
      </div>
    </AssistantRuntimeProvider>
  );
};