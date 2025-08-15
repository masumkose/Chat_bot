// components/project-card.tsx

import { Star, GitFork, ExternalLink } from "lucide-react";

// Proje verisinin tipini tanımlıyoruz
interface Repo {
  name: string;
  description: string;
  html_url: string;
  stargazers_count: number;
  forks_count: number;
  language: string;
}

interface ProjectCardProps {
  repo: Repo;
}

export const ProjectCard = ({ repo }: ProjectCardProps) => {
  return (
    <div className="flex flex-col justify-between h-full p-6 bg-white dark:bg-gray-950 border border-gray-200 dark:border-gray-800 rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300">
      <div>
        <div className="flex justify-between items-start mb-3">
          <h3 className="text-xl font-bold text-gray-900 dark:text-gray-100">
            {repo.name}
          </h3>
          <a
            href={repo.html_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-400 hover:text-blue-500 dark:hover:text-blue-400 transition-colors"
            aria-label={`View ${repo.name} on GitHub`}
          >
            <ExternalLink size={20} />
          </a>
        </div>
        <p className="text-gray-600 dark:text-gray-400 text-sm mb-4">
          {repo.description || "No description provided."}
        </p>
      </div>
      <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400 mt-4">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1">
            <Star size={16} className="text-yellow-500" />
            <span>{repo.stargazers_count}</span>
          </div>
          <div className="flex items-center gap-1">
            <GitFork size={16} className="text-gray-600 dark:text-gray-300" />
            <span>{repo.forks_count}</span>
          </div>
        </div>
        {repo.language && (
          <span className="px-2 py-1 bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-300 rounded-full text-xs font-medium">
            {repo.language}
          </span>
        )}
      </div>
    </div>
  );
};