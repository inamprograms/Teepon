'use client'
import React from 'react';

const CustomInput = ({ inputType, label, value, onChange, disabled }) => {
  return (
    <div className="flex items-center justify-between gap-4 w-full">
      <label htmlFor={label} className="font-medium text-sm">
        {label}
      </label>
      <input
        type={inputType}
        id={label.toLowerCase()}
        className={`border ${disabled ? 'border-transparent' : 'border-gray-300'}
          rounded-lg w-full px-3 py-2 mt-1 focus:outline-none focus:ring-2 focus:ring-gray-200`}
        value={value}
        onChange={onChange}
        disabled={disabled}
      />
    </div>
  );
};

export default CustomInput;
