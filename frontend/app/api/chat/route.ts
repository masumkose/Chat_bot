// bu benim frontend kodum ---> BU SON VE DOĞRU KODU KULLANIN

// ReadableStream'i Vercel AI formatına dönüştürmek için TextEncoder/Decoder kullanacağız.

export const runtime = "edge";
export const maxDuration = 30;

/**
 * Bu fonksiyon, backend'den gelen ham bir metin akışını (text/plain) alır
 * ve onu Vercel AI SDK'nın beklediği veri akışı formatına dönüştürür.
 * Her metin parçasının başına `0:` ekler ve sonuna bir newline karakteri koyar.
 * @param {ReadableStream<Uint8Array>} backendStream - FastAPI'den gelen ham akış.
 * @returns {Response} - Vercel AI SDK ile uyumlu, formatlanmış bir akış içeren Response nesnesi.
 */
function toVercelAiStream(backendStream: ReadableStream<Uint8Array>): Response {
  const textEncoder = new TextEncoder();
  const textDecoder = new TextDecoder();

  const transformStream = new TransformStream({
    async transform(chunk, controller) {
      // Gelen ham metin parçasını decode et
      const text = textDecoder.decode(chunk);

      // Vercel AI SDK formatına çevir: 0:"<içerik>"\n
      const formattedChunk = `0:"${JSON.stringify(text).slice(1, -1)}"\n`;
      
      // Formatlanmış parçayı tekrar encode edip akışa ekle
      controller.enqueue(textEncoder.encode(formattedChunk));
    },
  });

  // Gelen backend akışını, bizim transform akışımıza yönlendir (pipe).
  backendStream.pipeTo(transformStream.writable);

  // Dönüştürülmüş akışın okunabilir tarafını Response olarak döndür.
  return new Response(transformStream.readable, {
    headers: {
      // Content-Type'ı Vercel AI SDK'nın bekleidiği gibi ayarlıyoruz.
      'Content-Type': 'text/plain; charset=utf-8',
    },
  });
}


export async function POST(req: Request) {
  try {
    const { messages } = await req.json();

    const backendResponse = await fetch(`http://localhost:8000/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ messages }),
    });

    if (!backendResponse.ok) {
      const errorText = await backendResponse.text();
      console.error(`Backend Error: ${errorText}`);
      // Hata durumunda da frontend'e anlamlı bir hata mesajı döndür
      return new Response(errorText, { status: backendResponse.status });
    }

    if (!backendResponse.body) {
      return new Response('Backend returned an empty response stream', { status: 500 });
    }

    // --- EN ÖNEMLİ DEĞİŞİKLİK BURADA ---
    // Backend'den gelen ham akışı doğrudan döndürmek yerine,
    // onu Vercel AI formatına dönüştüren yardımcı fonksiyonumuzu çağırıyoruz.
    return toVercelAiStream(backendResponse.body);

  } catch (error) {
    console.error("Error in API route:", error);
    return new Response('An internal server error occurred.', { status: 500 });
  }
}