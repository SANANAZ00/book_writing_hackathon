import { useState, useCallback } from 'react';

// Translation service class for handling translation operations
class TranslationService {
  constructor() {
    // In a real app, this would connect to an actual translation API
    // For now, we'll use the same mock translations as in the context
    this.mockTranslations = {
      // Course introduction
      'intro': {
        title: 'متعارف Physical AI & Humanoid Robotics',
        content: 'Physical AI & Humanoid Robotics کورس میں خوش آمدید۔ یہ کورس جسمانی روبوٹکس اور مصنوعی ذہانت کے امتزاج کو سمجھنے کے لئے ڈیزائن کیا گیا ہے۔'
      },
      // Module 1: ROS 2
      'module-1-ros2': {
        title: 'روبوٹک نروس سسٹم (ROS 2)',
        content: 'ROS 2 کے بارے میں جانیں، جو روبوٹک اجزاء کے درمیان رابطے کو فعال کرنے والا وسط ہے۔'
      },
      // Module 2: Digital Twin
      'module-2-digital-twin': {
        title: 'ڈیجیٹل ٹوئن (گیزبو اور یونٹی)',
        content: 'روبوٹ کی شبیہ سازی کے لیے گیزبو اور یونٹی کا استعمال کرتے ہوئے ڈیجیٹل ٹوئن ٹیکنالوجیز کو سمجھیں۔'
      },
      // Module 3: AI Brain
      'module-3-ai-brain': {
        title: 'AI-روبٹ مغز (NVIDIA Isaac™)',
        content: 'AI پاورڈ روبوٹک ایپلی کیشنز تیار کرنے کے لیے NVIDIA Isaac™ پلیٹ فارم دریافت کریں۔'
      },
      // Module 4: VLA
      'module-4-vla': {
        title: 'وژن-لینگویج-ایکشن (VLA)',
        content: 'ان ماڈلز کو سمجھیں جو روبوٹس کو دیکھنے، سمجھنے اور کام کرنے کے قابل بناتے ہیں۔'
      },
      // Module 5: Weekly Breakdown
      'module-5-weekly-breakdown': {
        title: 'ہفتہ وار تقسیم',
        content: 'ہفتہ وار سیکھنے کا منصوبہ اور اہم نقاط کا جائزہ۔'
      },
      // Module 6: Capstone
      'module-6-capstone': {
        title: 'کیپ اسٹون پروجیکٹ',
        content: 'اپنی سیکھنے کی مہارتوں کو ظاہر کرنے کے لیے ایک مکمل روبوٹکس پروجیکٹ۔'
      },
      // Common UI elements
      'start-learning': {
        title: 'سیکھنا شروع کریں',
        content: 'ابھی سیکھنا شروع کریں'
      },
      'explore-modules': {
        title: 'ماڈیولز کا جائزہ لیں',
        content: 'ماڈیولز کا جائزہ لیں'
      },
      'ai-powered-learning': {
        title: 'AI پاورڈ سیکھنا',
        content: 'ذاتی نوعیت کی رہنمائی فراہم کرنے والے ذہین سسٹم کے ساتھ آپ کی سیکھنے کی سطح کے مطابق سیکھنا۔'
      },
      'real-world-applications': {
        title: 'حقیقی دنیا کی ایپلی کیشنز',
        content: 'ROS 2، گیزبو، یونٹی، اور NVIDIA Isaac جیسے صنعتی معیار کے ٹولز کا استعمال کرتے ہوئے اصل ہیومنوائڈ روبوٹس بنائیں اور اسے چلائیں۔'
      },
      'interactive-experience': {
        title: 'متحرک تجربہ',
        content: 'ہمارے AI اسسٹنٹ کے ساتھ ملو، اپنے سوالات کے فوری جوابات حاصل کریں، اور ہاتھوں سے سیکھنے کی سرگرمیوں میں حصہ لیں۔'
      },
      'comprehensive-curriculum': {
        title: 'جامع منصوبہ بندی',
        content: 'روبوٹکس کے بنیادی تصورات سے لے کر جسمانی سسٹمز میں اعلیٰ AI انضمام تک مکمل اختتام تک سیکھنے کا راستہ۔'
      },
      // Navigation and common terms
      'home': {
        title: 'ہوم',
        content: 'ہوم'
      },
      'modules': {
        title: 'ماڈیولز',
        content: 'ماڈیولز'
      },
      'about': {
        title: 'ہم about',
        content: 'ہم about'
      },
      'contact': {
        title: 'رابطہ',
        content: 'رابطہ'
      },
      // AI Assistant Lucy
      'lucy-welcome': {
        title: 'لیوسی میں خوش آمدید',
        content: 'لیوسی: آپ کا AI سیکھنے کا اسسٹنٹ'
      },
      'ask-question': {
        title: 'سوال پوچھیں',
        content: 'لیوسی سے سوال کریں'
      },
      'send': {
        title: 'بھیجیں',
        content: 'بھیجیں'
      },
      // Course-specific content
      'course-description': {
        title: 'کورس کی تفصیل',
        content: 'Physical AI & Humanoid Robotics کورس جسمانی روبوٹکس اور مصنوعی ذہانت کے امتزاج کو سمجھنے کے لئے ڈیزائن کیا گیا ہے۔'
      },
      'learning-path': {
        title: 'سیکھنے کا راستہ',
        content: 'ہمارا تدریجی سیکھنے کا راستہ صنعتی ماہرین کے ذریعہ ڈیزائن کیا گیا ہے۔'
      },
      'projects': {
        title: 'پروجیکٹس',
        content: 'ہاتھوں سے پروجیکٹس جو آپ کی مہارتوں کو بڑھانے میں مدد کریں گے۔'
      },
      'ai-support': {
        title: 'AI سپورٹ',
        content: '24/7 AI سپورٹ جو آپ کی رہنمائی کرے گی۔'
      }
    };

    this.translationCache = new Map();
  }

  // Translate content by ID
  translateContent(contentId, fallbackContent = null, isUrdu = false) {
    if (!isUrdu || !contentId) {
      return fallbackContent;
    }

    // Check cache first
    const cacheKey = `${contentId}_${isUrdu}`;
    if (this.translationCache.has(cacheKey)) {
      return this.translationCache.get(cacheKey);
    }

    const translation = this.mockTranslations[contentId];
    if (!translation) {
      return fallbackContent;
    }

    const result = {
      title: translation.title,
      content: translation.content
    };

    // Cache the result
    this.translationCache.set(cacheKey, result);
    return result;
  }

  // Get translated text for specific content
  getTranslation(contentId, fallbackText = '', isUrdu = false) {
    if (!isUrdu) {
      return fallbackText;
    }

    const translation = this.mockTranslations[contentId];
    return translation ? translation.content : fallbackText;
  }

  // Get translated title for specific content
  getTitleTranslation(contentId, fallbackTitle = '', isUrdu = false) {
    if (!isUrdu) {
      return fallbackTitle;
    }

    const translation = this.mockTranslations[contentId];
    return translation ? translation.title : fallbackTitle;
  }

  // Extract text content from React elements (simplified version)
  extractTextFromChildren(children) {
    if (typeof children === 'string') {
      return children;
    }
    if (typeof children === 'number') {
      return String(children);
    }
    if (Array.isArray(children)) {
      return children
        .map(child => this.extractTextFromChildren(child))
        .filter(Boolean)
        .join(' ');
    }
    if (children && typeof children === 'object' && children.props) {
      return this.extractTextFromChildren(children.props.children);
    }
    return '';
  }

  // Translate raw text (in a real app, this would call an actual API)
  async translateText(text, sourceLang = 'en', targetLang = 'ur') {
    // In a real implementation, this would call a translation API
    // For now, return the original text as we don't have actual translation
    return text;
  }

  // Get all available translation keys
  getAvailableTranslations() {
    return Object.keys(this.mockTranslations);
  }

  // Check if a specific content has translation
  hasTranslation(contentId) {
    return this.mockTranslations.hasOwnProperty(contentId);
  }

  // Clear translation cache
  clearCache() {
    this.translationCache.clear();
  }

  // Get translation statistics
  getStats() {
    return {
      totalTranslations: Object.keys(this.mockTranslations).length,
      cachedItems: this.translationCache.size,
      availableKeys: Object.keys(this.mockTranslations)
    };
  }
}

// React hook that wraps the translation service
export const useTranslationService = () => {
  const [isUrdu, setIsUrdu] = useState(false);
  const [translationService] = useState(() => new TranslationService());

  const toggleTranslation = useCallback(() => {
    setIsUrdu(prev => !prev);
  }, []);

  const translateContent = useCallback((contentId, fallbackContent = null) => {
    return translationService.translateContent(contentId, fallbackContent, isUrdu);
  }, [isUrdu, translationService]);

  const getTranslation = useCallback((contentId, fallbackText = '') => {
    return translationService.getTranslation(contentId, fallbackText, isUrdu);
  }, [isUrdu, translationService]);

  const getTitleTranslation = useCallback((contentId, fallbackTitle = '') => {
    return translationService.getTitleTranslation(contentId, fallbackTitle, isUrdu);
  }, [isUrdu, translationService]);

  const translateText = useCallback(async (text, sourceLang = 'en', targetLang = 'ur') => {
    return await translationService.translateText(text, sourceLang, targetLang);
  }, [translationService]);

  const hasTranslation = useCallback((contentId) => {
    return translationService.hasTranslation(contentId);
  }, [translationService]);

  const resetTranslation = useCallback(() => {
    setIsUrdu(false);
    translationService.clearCache();
  }, [translationService]);

  return {
    isUrdu,
    toggleTranslation,
    translateContent,
    getTranslation,
    getTitleTranslation,
    translateText,
    hasTranslation,
    resetTranslation,
    translationService,
    translationStats: translationService.getStats()
  };
};

// Higher-order component for translating content
export const withTranslation = (WrappedComponent, contentId) => {
  return (props) => {
    const { isUrdu, getTranslation, getTitleTranslation } = useTranslationService();

    const translatedProps = {
      ...props,
      originalContent: props.children,
      translatedContent: isUrdu ? getTranslation(contentId, props.children) : props.children,
      translatedTitle: isUrdu ? getTitleTranslation(contentId, props.title || '') : props.title
    };

    return <WrappedComponent {...translatedProps} />;
  };
};

// Default export of the service instance
export default new TranslationService();