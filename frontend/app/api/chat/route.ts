// app/api/chat/route.ts

import { AIStream, readableFromAsyncIterable } from 'ai';

const BACKEND_API_URL = 'http://localhost:8000/chat';

export const runtime = "edge";
export const maxDuration = 30;

// Bu yardımcı fonksiyon, bir metni alır ve kelimeleri
// küçük bir gecikmeyle teker teker "yield" ederek bir
// asenkron akış oluşturur.
async function* createWordStream(text: string) {
  const words = text.split(' ');
  for (const word of words) {
    yield word + ' ';
    await new Promise((resolve) => setTimeout(resolve, 30)); // "Yazıyor" efekti için gecikme
  }
}

export async function POST(req: Request) {
  const { messages } = await req.json();

  // Son kullanıcı mesajını alıyoruz. Backend'iniz sadece query bekliyor.
  const lastUserMessage = messages[messages.length - 1]?.content;

  if (!lastUserMessage) {
    return new Response("Mesaj bulunamadı.", { status: 400 });
  }

  try {
    // 1. Kendi backend'inize isteği gönderin ve tam yanıtı bekleyin.
    const response = await fetch(BACKEND_API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: lastUserMessage }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("Backend Hatası:", errorText);
      // Hata durumunda, hatayı metin olarak döndürerek frontend'de gösterilmesini sağlayabiliriz.
      return new Response(`Backend'den hata alındı: ${errorText}`, { status: response.status });
    }

    const resultJson = await response.json();
    const backendAnswer: string = resultJson.answer;

    if (typeof backendAnswer !== 'string') {
        throw new Error("Backend'den gelen 'answer' alanı bir metin değil.");
    }
    
    // ----- İSTEDİĞİNİZ DEĞİŞİKLİK BURADA BAŞLIYOR -----

    // 2. Backend'den gelen tam metni, kelime kelime stream edecek bir akışa dönüştür.
    const stream = readableFromAsyncIterable(createWordStream(backendAnswer));

    // 3. Bu ham metin akışını, AI SDK'nın frontend'de anlayacağı formata dönüştür.
    const aiStream = AIStream(stream);
    
    // 4. Sonucu, .toDataStreamResponse() ile aynı işi yapan standart Response ile döndür.
    return new Response(aiStream.stream, {
        headers: { "Content-Type": "text/plain; charset=utf-8" },
    });
    
    // ----- DEĞİŞİKLİK BURADA BİTİYOR -----

  } catch (error) {
    console.error("API rotasında bir hata oluştu:", error);
    return new Response("Sunucu tarafında bir hata oluştu.", { status: 500 });
  }
}