// app/page.tsx

import { Assistant } from "./assistant";
import { Button } from "@/components/ui/button";
import { ProjectCard } from "@/components/project-card";
import { ContactForm } from "@/components/contact-form";
import { ThemeToggleButton } from "@/components/theme-toggle-button";

// <<< FIX 2.1: Define a specific type for your GitHub repository object
type GithubRepo = {
  id: number;
  name: string;
  html_url: string;
  description: string;
  stargazers_count: number;
  forks_count: number;
  language: string;
};

// This function now returns a promise of an array of GithubRepo objects
async function getAllGithubProjects(username: string): Promise<GithubRepo[]> {
  // <<< FIX 2.2: Initialize the array with the correct type
  let allProjects: GithubRepo[] = [];
  let page = 1;
  const perPage = 100;

  try {
    while (true) {
      const res = await fetch(
        `https://api.github.com/users/${username}/repos?sort=updated&per_page=${perPage}&page=${page}`
      );
      
      if (!res.ok) {
        console.error("Failed to fetch GitHub repos:", res.statusText);
        break;
      }

      const projectsOnPage: GithubRepo[] = await res.json();
      
      if (projectsOnPage.length === 0) {
        break;
      }
      
      allProjects = allProjects.concat(projectsOnPage);
      page++;
    }
    return allProjects;
  } catch (error) {
    console.error("Error fetching GitHub projects:", error);
    return [];
  }
}

export default async function HomePage() {
  const username = "masumkose";
  const projects = await getAllGithubProjects(username);

  return (
    <main className="bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 min-h-screen">
      <div className="fixed top-6 right-6 z-50">
        <ThemeToggleButton />
      </div>
      {/* Hero Section */}
      <section className="text-center py-20 sm:py-32">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight">
            {/* <<< FIX 1.1: Replaced ' with &apos; */}
            Hi, I&apos;m Masum Köse
          </h1>
          <p className="mt-4 max-w-2xl mx-auto text-lg sm:text-xl text-gray-600 dark:text-gray-400">
            {/* <<< FIX 1.2: Replaced ' with &apos; */}
            I&apos;m a software developer creating innovative solutions. 
            Chat with my AI assistant below or explore my projects to learn more about me.
          </p>
          <div className="mt-8 flex justify-center gap-4">
            <Button size="lg" asChild>
              <a href="#projects">My Projects</a>
            </Button>
            <Button size="lg" variant="outline" asChild>
              <a href="#ai-assistant-section">Chat with AI Assistant</a>
            </Button>
          </div>
        </div>
      </section>

      {/* AI Assistant Section */}
      <section id="ai-assistant-section" className="py-20 sm:py-24 bg-white dark:bg-black/20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold">Meet My AI Assistant</h2>
            <p className="mt-3 max-w-xl mx-auto text-md text-gray-500 dark:text-gray-400">
              You can ask my assistant anything about my projects, technical skills, or experience. 
              It provides instant answers based on my documents thanks to the RAG pipeline in the backend.
            </p>
          </div>
          <div className="max-w-3xl mx-auto h-[600px] border dark:border-gray-700 rounded-xl shadow-2xl overflow-hidden flex flex-col">
            <Assistant />
          </div>
        </div>
      </section>
      
      {/* Projects Section */}
      <section id="projects" className="py-20 sm:py-24">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold">My Projects</h2>
            <p className="mt-3 max-w-xl mx-auto text-md text-gray-500 dark:text-gray-400">
              Here are all of my public repositories from GitHub.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {projects && projects.length > 0 ? (
              // <<< FIX 2.3: Use the specific GithubRepo type instead of 'any'
              projects.map((repo: GithubRepo) => (
                <ProjectCard key={repo.id} repo={repo} />
              ))
            ) : (
              <p className="md:col-span-2 lg:col-span-3 text-center text-gray-500">
                Could not load projects from GitHub. Please check the console for errors.
              </p>
            )}
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-20 sm:py-24">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold">Get In Touch</h2>
            <p className="mt-3 max-w-xl mx-auto text-md text-gray-500 dark:text-gray-400">
              Have a question or want to work together? Feel free to send me a message.
            </p>
          </div>
          <div className="max-w-xl mx-auto">
            <ContactForm />
          </div>
        </div>
      </section>
    </main>
  );
}