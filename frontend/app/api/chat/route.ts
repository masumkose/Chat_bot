
export const runtime = "edge";
export const maxDuration = 30;

/**
 * Converts a raw text stream (text/plain) from the backend
 * into the format expected by the Vercel AI SDK.
 * Each text chunk is prefixed with `0:` and suffixed with a newline.
 * @param {ReadableStream<Uint8Array>} backendStream - Raw stream from FastAPI.
 * @returns {Response} - Response object containing the formatted stream.
 */
function toVercelAiStream(backendStream: ReadableStream<Uint8Array>): Response {
  const textEncoder = new TextEncoder();
  const textDecoder = new TextDecoder();

  const transformStream = new TransformStream({
    async transform(chunk, controller) {
      const text = textDecoder.decode(chunk);
      const formattedChunk = `0:"${JSON.stringify(text).slice(1, -1)}"\n`;
      controller.enqueue(textEncoder.encode(formattedChunk));
    },
  });

  backendStream.pipeTo(transformStream.writable);

  return new Response(transformStream.readable, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
    },
  });
}

export async function POST(req: Request) {
  try {
    const { messages } = await req.json();

    const backendResponse = await fetch(`${process.env.BACKEND_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ messages }),
    });

    if (!backendResponse.ok) {
      const errorText = await backendResponse.text();
      console.error(`Backend Error: ${errorText}`);
      return new Response(errorText, { status: backendResponse.status });
    }

    if (!backendResponse.body) {
      return new Response('Backend returned an empty response stream', { status: 500 });
    }

    // Instead of returning the raw backend stream,
    // we convert it to the Vercel AI format.
    return toVercelAiStream(backendResponse.body);

  } catch (error) {
    console.error("Error in API route:", error);
    return new Response('An internal server error occurred.', { status: 500 });
  }
}
