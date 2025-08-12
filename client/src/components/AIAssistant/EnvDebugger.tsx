import { useEffect } from 'react';

/**
 * This component doesn't render anything, it just logs environment variables
 * to help debug issues with environment variables not loading correctly.
 */
const EnvDebugger = () => {
  useEffect(() => {
    // 检查环境变量
    console.log('===== ENV VARIABLES DEBUGGER =====');
    console.log('All Vite env vars:', import.meta.env);
    console.log('VITE_OPENAI_API_KEY exists:', !!import.meta.env.VITE_OPENAI_API_KEY);
    console.log('VITE_OPENAI_MODEL:', import.meta.env.VITE_OPENAI_MODEL || 'Not set');
    
    // 如果有密钥，检查格式
    const apiKey = import.meta.env.VITE_OPENAI_API_KEY;
    if (apiKey) {
      console.log('API key starts with:', apiKey.substring(0, 5) + '...');
      console.log('API key length:', apiKey.length);
      console.log('API key format valid:', apiKey.startsWith('sk-') && apiKey.length > 20);
    } else {
      console.log('No API key found');
    }
    console.log('==================================');
  }, []);

  return null;
};

export default EnvDebugger; 