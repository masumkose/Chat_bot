// components/contact-form.tsx
"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

export const ContactForm = () => {
  const [status, setStatus] = useState("");

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    // Ensure the environment variable is loaded
    const formspreeUrl = process.env.NEXT_PUBLIC_FORMSPREE_URL;
    if (!formspreeUrl) {
      setStatus("Configuration error: Form URL is missing.");
      return;
    }

    setStatus("Sending...");
    const form = e.currentTarget;
    const data = new FormData(form);
    
    try {
      // --- UPDATE THIS LINE ---
      const response = await fetch(formspreeUrl, {
      // ------------------------
        method: "POST",
        body: data,
        headers: {
          'Accept': 'application/json'
        }
      });

      if (response.ok) {
        setStatus("Thanks for your message!");
        form.reset();
      } else {
        setStatus("Oops! There was a problem submitting your form.");
      }
    } catch (error) {
      setStatus("Oops! There was a problem submitting your form.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Input type="text" name="name" placeholder="Your Name" required className="bg-white dark:bg-gray-800" />
        <Input type="email" name="email" placeholder="Your Email" required className="bg-white dark:bg-gray-800" />
      </div>
      <Textarea name="message" placeholder="Your Message" required rows={5} className="bg-white dark:bg-gray-800" />
      <div className="flex justify-end">
        <Button type="submit" disabled={status === "Sending..."}>
          {status === "Sending..." ? "Sending..." : "Send Message"}
        </Button>
      </div>
      {status && <p className="text-center mt-4 text-sm">{status}</p>}
    </form>
  );
};