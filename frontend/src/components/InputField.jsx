import { useState, forwardRef } from 'react';
import './InputField.css';

const InputField = forwardRef(({
  label,
  type = 'text',
  error,
  className = '',
  required = false,
  value,
  onBlur,
  ...props
}, ref) => {
  const [isFocused, setIsFocused] = useState(false);
  const isFloated = isFocused || (value !== undefined && value !== '');

  return (
    <div className={`field-group ${className}`}>
      <div className={`field-wrapper ${isFocused ? 'field-focused' : ''} ${error ? 'field-error-state' : ''}`}>
        <input
          ref={ref}
          type={type}
          className="field-input"
          value={value}
          placeholder=" "
          aria-invalid={error ? 'true' : 'false'}
          aria-describedby={error ? `${props.id}-error` : undefined}
          onFocus={() => setIsFocused(true)}
          onBlur={(e) => {
            setIsFocused(false);
            onBlur?.(e);
          }}
          {...props}
        />
        {label && (
          <label htmlFor={props.id} className={`field-label ${isFloated ? 'field-label-floated' : ''}`}>
            {label}
            {required && <span className="required-mark" aria-hidden="true"> *</span>}
          </label>
        )}
      </div>
      {error && (
        <span
          id={`${props.id}-error`}
          className="field-error-message animate-slide-down"
          role="alert"
        >
          {error}
        </span>
      )}
    </div>
  );
});

InputField.displayName = 'InputField';

export default InputField;
