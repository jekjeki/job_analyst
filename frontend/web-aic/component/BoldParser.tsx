import React from 'react'


const BoldTextParser = ({ text }) => {
    const parseBoldText = (inputText) => {
      const parts = inputText.split(/(\*\*"[^"]+"\*\*|\*\*[^*]+\*\*)/);
      return parts.map((part, index) => {
        if (part.startsWith('**"') && part.endsWith('**')) {
          // Bold text with quotes
          const innerText = part.slice(3, -3);
          return <b key={index}>"{innerText}"</b>;
        } else if (part.startsWith('**') && part.endsWith('**')) {
          // Regular bold text
          const innerText = part.slice(2, -2);
          return <b key={index}>{innerText}</b>;
        }
        // Regular text
        return part;
      });
    };
  
    return <>{parseBoldText(text)}</>;
  };
  
  export default BoldTextParser;
  