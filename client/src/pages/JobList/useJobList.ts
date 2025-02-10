// useJobList.ts
import { useQuery } from '@tanstack/react-query';

// Job type interface
export interface Job {
  id: string;
  title: string;
  company: string;
  job_type: string;
  created_at: string;
  updated_at: string;
  description: string;
}

// Mocked job data for 20 jobs
export const mockJobs: Job[] = [
  {
    id: "1",
    title: "Senior Full Stack Developer",
    company: "TechCorp",
    job_type: "ft",
    created_at: "2024-09-01",
    updated_at: "2024-09-15",
    description: `We are seeking a highly skilled Senior Full Stack Developer to join our dynamic team. The ideal candidate will have a strong background in both front-end and back-end development, with a passion for creating efficient, scalable, and maintainable code.

**Required Skills and Experience:**

- 5+ years of experience in full stack development
- Proficiency in JavaScript, HTML5, and CSS3
- Strong experience with React.js and Node.js
- Familiarity with database technologies (MySQL, MongoDB)
- Experience with RESTful APIs and microservices architecture
- Knowledge of cloud platforms (AWS or Azure)
- Version control with Git
- Agile development methodologies
- Strong problem-solving and analytical skills
- Excellent communication and teamwork abilities

**Nice to Have:**

- Experience with TypeScript
- Familiarity with Docker and Kubernetes
- Knowledge of GraphQL
- Experience with CI/CD pipelines
- Understanding of DevOps practices

**Responsibilities:**

- Develop and maintain web applications using modern JavaScript frameworks
- Collaborate with cross-functional teams to define and implement new features
- Optimize applications for maximum speed and scalability
- Participate in code reviews and contribute to team best practices
- Troubleshoot, debug, and upgrade existing software
- Stay up-to-date with emerging trends and technologies in web development

If you are passionate about creating high-quality software and thrive in a collaborative environment, we want to hear from you!`,
  },
  {
    id: "2",
    title: "Backend Engineer",
    company: "InnovateIT",
    job_type: "ft",
    created_at: "2024-08-12",
    updated_at: "2024-09-14",
    description:
      "InnovateIT is seeking a skilled Backend Engineer to develop and optimize server-side logic, APIs, and database structures. You'll collaborate with frontend developers to integrate web applications.",
  },
  {
    id: "3",
    title: "Data Analyst",
    company: "DataWorks",
    job_type: "pt",
    created_at: "2024-08-10",
    updated_at: "2024-09-10",
    description:
      "Analyze data sets and generate actionable insights for our clients at DataWorks. You'll be responsible for creating dashboards, performing statistical analyses, and providing key business recommendations.",
  },
  {
    id: "4",
    title: "UI/UX Designer",
    company: "Creative Inc.",
    job_type: "ft",
    created_at: "2024-09-03",
    updated_at: "2024-09-17",
    description:
      "As a UI/UX Designer at Creative Inc., you will design user interfaces and craft user experiences for web and mobile applications. Work with a talented design and development team to ensure intuitive, impactful designs.",
  },
  {
    id: "5",
    title: "DevOps Engineer",
    company: "CloudBase",
    job_type: "ft",
    created_at: "2024-08-01",
    updated_at: "2024-09-20",
    description:
      "CloudBase is hiring a DevOps Engineer to manage cloud infrastructure, automate deployment pipelines, and enhance system scalability. You'll work with AWS, Docker, and Kubernetes.",
  },
  {
    id: "6",
    title: "Product Manager",
    company: "StartUp XYZ",
    job_type: "ct",
    created_at: "2024-07-25",
    updated_at: "2024-09-12",
    description:
      "Lead product development at StartUp XYZ as a Product Manager. You will define product vision, prioritize features, and collaborate with cross-functional teams to deliver customer-focused solutions.",
  },
  {
    id: "7",
    title: "Mobile App Developer",
    company: "MobileGen",
    job_type: "ft",
    created_at: "2024-07-15",
    updated_at: "2024-09-19",
    description:
      "MobileGen seeks a Mobile App Developer to build native mobile applications for Android and iOS. You'll work with React Native and Swift/Java to create fast and user-friendly apps.",
  },
  {
    id: "8",
    title: "Marketing Specialist",
    company: "BrandBoost",
    job_type: "pt",
    created_at: "2024-08-30",
    updated_at: "2024-09-21",
    description:
      "Boost your career at BrandBoost by leading marketing campaigns, managing social media accounts, and developing content strategies to enhance brand visibility and engagement across platforms.",
  },
  {
    id: "9",
    title: "Cybersecurity Analyst",
    company: "SecureTech",
    job_type: "ft",
    created_at: "2024-06-05",
    updated_at: "2024-09-18",
    description:
      "As a Cybersecurity Analyst at SecureTech, you'll monitor systems for security breaches, implement security measures, and ensure compliance with security standards to protect sensitive data.",
  },
  {
    id: "10",
    title: "Full Stack Developer",
    company: "DevHouse",
    job_type: "ft",
    created_at: "2024-09-10",
    updated_at: "2024-09-25",
    description:
      "DevHouse is looking for a Full Stack Developer to work on both frontend and backend tasks. You'll develop full-scale web applications using JavaScript, Node.js, and SQL databases.",
  },
  {
    id: "11",
    title: "Software Tester",
    company: "QATeam",
    job_type: "ct",
    created_at: "2024-08-11",
    updated_at: "2024-09-22",
    description:
      "Join QATeam as a Software Tester to ensure the quality of software products through manual and automated testing. You'll identify bugs, write test cases, and work with developers to resolve issues.",
  },
  {
    id: "12",
    title: "Cloud Architect",
    company: "SkyNet",
    job_type: "ft",
    created_at: "2024-07-28",
    updated_at: "2024-09-24",
    description:
      "Design and manage cloud solutions as a Cloud Architect at SkyNet. You will be responsible for building secure, scalable cloud infrastructures using AWS and Azure.",
  },
  {
    id: "13",
    title: "Machine Learning Engineer",
    company: "AI Innovations",
    job_type: "ft",
    created_at: "2024-09-05",
    updated_at: "2024-09-27",
    description:
      "AI Innovations is hiring a Machine Learning Engineer to design, build, and optimize machine learning models. You'll work with big data, neural networks, and AI to solve real-world problems.",
  },
  {
    id: "14",
    title: "Business Analyst",
    company: "Biz Solutions",
    job_type: "ft",
    created_at: "2024-08-15",
    updated_at: "2024-09-23",
    description:
      "Analyze business processes and recommend improvements as a Business Analyst at Biz Solutions. You will work with stakeholders to gather requirements and document workflows for various projects.",
  },
  {
    id: "15",
    title: "Systems Administrator",
    company: "NetManage",
    job_type: "ct",
    created_at: "2024-07-30",
    updated_at: "2024-09-26",
    description:
      "NetManage is seeking a Systems Administrator to maintain and support the company's IT infrastructure. Responsibilities include server management, network configurations, and security updates.",
  },
  {
    id: "16",
    title: "Technical Writer",
    company: "DocuTech",
    job_type: "pt",
    created_at: "2024-08-20",
    updated_at: "2024-09-28",
    description:
      "DocuTech is looking for a Technical Writer to create and maintain technical documentation, user manuals, and API guides. You'll translate complex technical concepts into easy-to-understand content.",
  },
  {
    id: "17",
    title: "Scrum Master",
    company: "AgileWorks",
    job_type: "ft",
    created_at: "2024-07-12",
    updated_at: "2024-09-11",
    description:
      "As a Scrum Master at AgileWorks, you will lead agile teams in the software development lifecycle, facilitate sprint planning, daily stand-ups, and ensure smooth project execution.",
  },
  {
    id: "18",
    title: "SEO Specialist",
    company: "WebOpt",
    job_type: "pt",
    created_at: "2024-08-08",
    updated_at: "2024-09-13",
    description:
      "WebOpt is looking for an SEO Specialist to optimize websites for search engines. You will conduct keyword research, optimize on-page elements, and monitor website performance using SEO tools.",
  },
  {
    id: "19",
    title: "Graphic Designer",
    company: "DesignPro",
    job_type: "ct",
    created_at: "2024-09-09",
    updated_at: "2024-09-21",
    description:
      "As a Graphic Designer at DesignPro, you'll create visually compelling designs for digital and print media. Collaborate with marketing teams to ensure brand consistency across platforms.",
  },
  {
    id: "20",
    title: "Data Scientist",
    company: "DataDriven",
    job_type: "ft",
    created_at: "2024-09-06",
    updated_at: "2024-09-25",
    description:
      "Join DataDriven as a Data Scientist to analyze large datasets and build predictive models. You will work with Python, R, and machine learning frameworks to provide data-driven insights.",
  },
];

// Custom hook to fetch job data
export function useJobList(email: string) {
  const {
    isLoading,
    data: job_list,
    error,
  } = useQuery<Job[], Error>({
    queryKey: ["jobs", email],
    queryFn: () => new Promise((resolve) => resolve(mockJobs)), // Mocked data
  });

  return {
    isLoading,
    job_list,
    error,
  };
}
