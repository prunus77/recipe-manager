import React from 'react';

const TagFilter = ({ tags, selectedTag, onSelectTag }) => {
  return (
    <div className="flex gap-2 py-4">
      {tags.map(tag => (
        <button
          key={tag}
          className={`px-3 py-1 rounded-full border ${selectedTag === tag ? 'bg-blue-500 text-white' : 'bg-white text-blue-500'}`}
          onClick={() => onSelectTag(tag)}
        >
          {tag}
        </button>
      ))}
    </div>
  );
};

export default TagFilter;
