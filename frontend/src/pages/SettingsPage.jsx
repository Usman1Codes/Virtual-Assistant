import { useState, useEffect, useCallback } from 'react';
import * as api from '../apiService';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { CheckCircle, Plus, Trash2, Loader2 } from 'lucide-react';

// Animation variants
const containerVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.1 } },
};

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: { y: 0, opacity: 1 },
};

export default function SettingsPage() {
  const [businessQuestions, setBusinessQuestions] = useState([]);
  const [settings, setSettings] = useState({});
  const [customerQuestions, setCustomerQuestions] = useState([]);
  const [newCustomerQuestion, setNewCustomerQuestion] = useState('');
  const [loading, setLoading] = useState(true);

  // --- Data Fetching ---
  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const [bizQuestionsRes, settingsRes, custQuestionsRes] = await Promise.all([
        api.getQuestions('business'),
        api.getSettings(),
        api.getQuestions('customer'),
      ]);
      
      setBusinessQuestions(bizQuestionsRes.data);
      // Convert settings array to a more useful map: { question_id: value }
      const settingsMap = settingsRes.data.reduce((acc, setting) => {
        acc[setting.question_id] = setting.value;
        return acc;
      }, {});
      setSettings(settingsMap);
      setCustomerQuestions(custQuestionsRes.data);

    } catch (error) {
      toast.error('Failed to load settings. Please refresh.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // --- Event Handlers ---
  const handleSettingChange = (questionId, value) => {
    setSettings(prev => ({ ...prev, [questionId]: value }));
  };

  const handleSaveSetting = async (questionId) => {
    const value = settings[questionId] || '';
    if (!value.trim()) {
      toast.error("This setting cannot be empty.");
      return;
    }
    const toastId = toast.loading('Saving...');
    try {
      await api.saveSetting({ question_id: questionId, value });
      toast.success('Setting saved!', { id: toastId });
    } catch (error) {
      toast.error('Could not save setting.', { id: toastId });
    }
  };

  const handleAddCustomerQuestion = async (e) => {
    e.preventDefault();
    if (!newCustomerQuestion.trim()) return;
    const toastId = toast.loading('Adding question...');
    try {
      const response = await api.createQuestion({ text: newCustomerQuestion, category: 'customer' });
      setNewCustomerQuestion('');
      // Instead of refetching, we add the new question directly to our local state
      setCustomerQuestions(prev => [...prev, response.data]);
      toast.success('Question added!', { id: toastId });
    } catch (error) {
      toast.error('Could not add question.', { id: toastId });
    }
  };

  const handleDeleteCustomerQuestion = async (questionId) => {
    const toastId = toast.loading('Deleting...');
    try {
      await api.deleteQuestion(questionId);
      // Instead of refetching, we filter the deleted question out of our local state
      setCustomerQuestions(prev => prev.filter(q => q.id !== questionId));
      toast.success('Question deleted!', { id: toastId });
    } catch (error) {
      toast.error('Could not delete question.', { id: toastId });
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-full">
        <Loader2 className="animate-spin text-primary" size={48} />
      </div>
    );
  }

  return (
    <motion.div initial="hidden" animate="visible" variants={containerVariants} className="space-y-12">
      {/* --- Business Profile Section --- */}
      <motion.section variants={itemVariants}>
        <h1 className="text-3xl font-bold text-text-main mb-2">Business Profile</h1>
        <p className="text-text-secondary mb-6">Define your assistant's identity and core settings.</p>
        <div className="space-y-6">
          {businessQuestions.map((q) => (
            <div key={q.id}>
              <label className="block text-lg font-semibold text-text-main mb-2">{q.text}</label>
              <div className="flex items-center space-x-3">
                <input
                  type="text"
                  value={settings[q.id] || ''}
                  onChange={(e) => handleSettingChange(q.id, e.target.value)}
                  onBlur={() => handleSaveSetting(q.id)}
                  className="flex-grow p-3 bg-surface rounded-md text-text-main focus:outline-none focus:ring-2 focus:ring-primary"
                />
              </div>
            </div>
          ))}
        </div>
      </motion.section>

      {/* --- Customer Questions Section --- */}
      <motion.section variants={itemVariants}>
        <h2 className="text-3xl font-bold text-text-main mb-2">Customer Questions</h2>
        <p className="text-text-secondary mb-6">Manage the questions your assistant will ask customers.</p>
        
        {/* Form to add new question */}
        <form onSubmit={handleAddCustomerQuestion} className="flex gap-4 mb-8">
          <input
            type="text"
            value={newCustomerQuestion}
            onChange={(e) => setNewCustomerQuestion(e.target.value)}
            placeholder="e.g., What is your order number?"
            className="flex-grow p-3 bg-surface rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
          />
          <button
            type="submit"
            className="bg-primary text-background font-bold p-3 rounded-md flex items-center justify-center hover:bg-primary/80 transition-colors"
          >
            <Plus size={24} />
          </button>
        </form>

        {/* List of existing questions */}
        <div className="space-y-3">
          {customerQuestions.map((q) => (
            <motion.div
              key={q.id}
              layout
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="flex items-center justify-between bg-surface p-4 rounded-lg"
            >
              <p className="text-text-main">{q.text}</p>
              <button
                onClick={() => handleDeleteCustomerQuestion(q.id)}
                className="text-text-secondary hover:text-red-500 transition-colors"
              >
                <Trash2 size={20} />
              </button>
            </motion.div>
          ))}
          {customerQuestions.length === 0 && (
            <p className="text-text-secondary text-center py-4">No customer questions configured yet.</p>
          )}
        </div>
      </motion.section>
    </motion.div>
  );
}