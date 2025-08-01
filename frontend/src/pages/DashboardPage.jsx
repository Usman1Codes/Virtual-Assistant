import { useState, useEffect, useCallback } from 'react';
import * as api from '../apiService';
import { motion, AnimatePresence } from 'framer-motion';
import toast from 'react-hot-toast';
import { Loader2, RefreshCw, MessageSquare, CheckCircle, Clock } from 'lucide-react';

export default function DashboardPage() {
  const [conversations, setConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchData = useCallback(async (isRefresh = false) => {
    if (!isRefresh) setLoading(true);
    const toastId = isRefresh ? toast.loading('Refreshing...') : undefined;
    
    try {
      const response = await api.getConversations();
      setConversations(response.data);
      if (selectedConversation) {
        // Reselect the conversation to get updated messages
        const updatedConversation = response.data.find(c => c.id === selectedConversation.id);
        setSelectedConversation(updatedConversation || null);
      }
    } catch (error) {
      toast.error('Failed to load conversations.');
      console.error(error);
    } finally {
      if (!isRefresh) setLoading(false);
      if (toastId) toast.dismiss(toastId);
    }
  }, [selectedConversation]);

  useEffect(() => {
    fetchData();
  }, []);

  const handleSelectConversation = (conversation) => {
    setSelectedConversation(conversation);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-full">
        <Loader2 className="animate-spin text-primary" size={48} />
      </div>
    );
  }

  return (
    <div className="flex h-full max-h-[calc(100vh-4rem)]">
      {/* Left Panel: Conversation List */}
      <aside className="w-1/3 min-w-[300px] bg-surface/50 rounded-lg overflow-y-auto p-4">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-2xl font-bold text-text-main">Conversations</h1>
          <button
            onClick={() => fetchData(true)}
            className="text-text-secondary hover:text-primary transition-colors"
          >
            <RefreshCw size={20} />
          </button>
        </div>
        <div className="space-y-2">
          {conversations.map((convo) => (
            <motion.div
              key={convo.id}
              onClick={() => handleSelectConversation(convo)}
              className={`p-4 rounded-lg cursor-pointer transition-colors ${
                selectedConversation?.id === convo.id ? 'bg-primary/20' : 'hover:bg-surface'
              }`}
              layout
            >
              <div className="flex justify-between items-center">
                <p className="font-semibold text-text-main truncate">{convo.customer_email}</p>
                {convo.status === 'completed' ? (
                  <CheckCircle className="text-green-500" size={18} />
                ) : (
                  <Clock className="text-yellow-500" size={18} />
                )}
              </div>
              <p className="text-sm text-text-secondary">
                {convo.messages.length} messages
              </p>
            </motion.div>
          ))}
        </div>
      </aside>

      {/* Right Panel: Message Details */}
      <main className="flex-1 p-6 ml-4 bg-surface/50 rounded-lg flex flex-col">
        <AnimatePresence>
          {selectedConversation ? (
            <motion.div
              key={selectedConversation.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="flex flex-col h-full"
            >
              <h2 className="text-xl font-bold text-text-main border-b border-surface pb-4 mb-4">
                Chat with {selectedConversation.customer_email}
              </h2>
              <div className="flex-1 overflow-y-auto space-y-6 pr-4">
                {[...selectedConversation.messages]
                  .sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
                  .map((msg) => (
                  <div key={msg.id} className={`flex ${msg.sender === 'assistant' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`p-4 rounded-lg max-w-lg ${
                      msg.sender === 'assistant'
                        ? 'bg-primary/20 text-text-main'
                        : 'bg-surface text-text-secondary'
                    }`}>
                      <p className="whitespace-pre-wrap">{msg.content}</p>
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>
          ) : (
            <div className="flex flex-col justify-center items-center h-full text-text-secondary">
              <MessageSquare size={64} />
              <p className="mt-4 text-xl">Select a conversation to view messages</p>
            </div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}