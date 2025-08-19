// frontend/app/assistant.tsx
"use client";

import { AssistantRuntimeProvider } from "@assistant-ui/react";
import { useChatRuntime } from "@assistant-ui/react-ai-sdk";
import { Thread } from "@/components/assistant-ui/thread";
import { useEffect, useState } from "react";
import { Loader2 } from "lucide-react"; // A loading spinner icon

// A simple state for our backend status
type BackendStatus = 'waking' | 'ready' | 'error';

export const Assistant = () => {
  const [backendStatus, setBackendStatus] = useState<BackendStatus>('waking');

  // This effect runs once on component mount to wake up the backend.
  useEffect(() => {
    const wakeUpBackend = async () => {
      try {
        const healthUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
        if (!healthUrl) {
          throw new Error("Backend URL is not configured.");
        }
        
        await fetch(`${healthUrl}/health`);

        // If the health check succeeds, the backend is ready.
        setBackendStatus('ready');

      } catch (error) {
        console.error("Backend wake-up failed:", error);
        // If it fails, set the error state.
        setBackendStatus('error');
      }
    };

    wakeUpBackend();
  }, []); // Empty dependency array ensures this runs only once

  const runtime = useChatRuntime({
    api: "/api/chat",
  });

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      {/* This container needs 'relative' for the overlay to be positioned correctly */}
      <div className="relative flex h-full flex-col">
        
        {/* The Overlay: This div only renders if the backend is not ready. */}
        {/* Its z-index ensures it sits on top of the Thread component, blocking clicks. */}
        {backendStatus !== 'ready' && (
          <div className="absolute inset-0 z-10 flex flex-col items-center justify-center bg-white/80 dark:bg-gray-950/80 backdrop-blur-sm">
            {backendStatus === 'waking' && (
              <>
                <Loader2 className="h-8 w-8 animate-spin text-gray-500" />
                <p className="mt-4 text-center text-gray-700 dark:text-gray-300">
                  Waking up the AI assistant...<br/>this may take a moment.
                </p>
              </>
            )}
            {backendStatus === 'error' && (
              <p className="text-center text-red-500 dark:text-red-400">
                Sorry, I couldn&rsquo;t connect to the AI assistant.<br/>Please try refreshing the page.
              </p>
            )}
          </div>
        )}

        {/* The Chat Thread: It is plain and has no special props. */}
        {/* It is rendered underneath the overlay. */}
        <Thread />
      </div>
    </AssistantRuntimeProvider>
  );
};