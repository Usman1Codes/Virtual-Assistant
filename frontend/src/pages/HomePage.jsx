import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { LogIn, ExternalLink, Bot, Mail, Sheet, BrainCircuit } from 'lucide-react';
import * as api from '../apiService';
import { ShowcaseGraphic, InjectColors } from '../components/ShowcaseGraphic';

// Animation variants for Framer Motion
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.15,
    },
  },
};

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: { y: 0, opacity: 1, transition: { type: 'spring', stiffness: 100 } },
};

const FeatureCard = ({ icon, title, description }) => (
  <motion.div variants={itemVariants} className="flex items-start space-x-4">
    <div className="bg-surface p-3 rounded-lg text-primary">{icon}</div>
    <div>
      <h3 className="font-bold text-lg text-text-main">{title}</h3>
      <p className="text-text-secondary">{description}</p>
    </div>
  </motion.div>
);

export default function HomePage() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await api.getAuthStatus();
        setIsAuthenticated(response.data.authenticated);
      } catch (error) {
        console.error("Error checking auth status:", error);
        setIsAuthenticated(false);
      } finally {
        setIsLoading(false);
      }
    };
    checkAuth();
  }, []);

  const AuthButton = () => {
    if (isLoading) {
      return (
        <div className="bg-primary/50 text-background font-bold text-lg px-12 py-4 rounded-lg shadow-lg flex items-center justify-center">
          Checking Status...
        </div>
      );
    }

    if (isAuthenticated) {
      return (
        <Link
          to="/dashboard"
          className="inline-block bg-primary text-background font-bold text-lg px-12 py-4 rounded-lg shadow-lg hover:bg-primary/80 transition-transform duration-200 hover:scale-105 flex items-center space-x-2"
        >
          <LogIn size={24} />
          <span>Go to Dashboard</span>
        </Link>
      );
    }

    return (
      <a
        href="http://localhost:8000/auth/google"
        className="inline-block bg-primary text-background font-bold text-lg px-12 py-4 rounded-lg shadow-lg hover:bg-primary/80 transition-transform duration-200 hover:scale-105 flex items-center space-x-2"
      >
        <ExternalLink size={24} />
        <span>Sign In with Google</span>
      </a>
    );
  };

  return (
    <>
      <InjectColors />
      <div className="min-h-screen bg-background w-full flex items-center justify-center p-8 overflow-hidden">
        <div className="w-full max-w-7xl grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
          
          {/* Left Side: Integrated Showcase */}
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="space-y-10"
          >
            <motion.div variants={itemVariants}>
              <ShowcaseGraphic />
            </motion.div>
            
            <div className="space-y-6">
              <FeatureCard
                icon={<Mail size={24} />}
                title="Automated Email Handling"
                description="Responds to customer inquiries and carries out conversations automatically."
              />
              <FeatureCard
                icon={<BrainCircuit size={24} />}
                title="Intelligent Conversations"
                description="Uses AI to understand context, ask clarifying questions, and gather required information."
              />
              <FeatureCard
                icon={<Sheet size={24} />}
                title="Seamless Data Entry"
                description="Automatically populates Google Sheets with validated data upon conversation completion."
              />
            </div>
          </motion.div>

          {/* Right Side: The Gateway */}
          <motion.div 
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2, duration: 0.8, ease: "easeOut" }}
            className="flex flex-col text-left"
          >
            <h1 className="text-5xl md:text-6xl font-bold text-text-main leading-tight mb-4">
              Automate.<br/>Integrate.<br/>Elevate.
            </h1>
            <p className="text-text-secondary text-lg max-w-md mb-8">
              Our autonomous AI assistant handles customer emails, gathers critical data, and seamlessly integrates with your workflow, freeing you to focus on your business.
            </p>
            <div className="mt-4">
              <AuthButton />
            </div>
          </motion.div>
        </div>
      </div>
    </>
  );
}