import { useState, forwardRef } from 'react';
import './PasswordInput.css';

const calculateStrength = (password) => {
  if (!password) return 0;
  let score = 0;
  if (password.length >= 8) score++;
  if (password.length >= 12) score++;
  if (/[a-z]/.test(password) && /[A-Z]/.test(password)) score++;
  if (/\d/.test(password)) score++;
  if (/[^a-zA-Z0-9]/.test(password)) score++;
  return Math.min(score, 4);
};

const STRENGTH_LABELS = ['', 'Weak', 'Fair', 'Good', 'Strong'];
const STRENGTH_COLORS = ['', '#C0392B', '#E07B39', '#C4B93E', '#1A8917'];

const PasswordInput = forwardRef(({
  label,
  error,
  showStrength = false,
  className = '',
  required = false,
  value,
  onBlur,
  onChange,
  ...props
}, ref) => {
  const [showPassword, setShowPassword] = useState(false);
  const [isFocused, setIsFocused] = useState(false);
  const strength = showStrength ? calculateStrength(value) : 0;
  const isFloated = isFocused || (value !== undefined && value !== '');

  const handleChange = (e) => {
    onChange?.(e);
  };

  return (
    <div className={`field-group ${className}`}>
      <div className={`field-wrapper ${isFocused ? 'field-focused' : ''} ${error ? 'field-error-state' : ''}`}>
        <input
          ref={ref}
          type={showPassword ? 'text' : 'password'}
          className="field-input field-input-password"
          value={value}
          placeholder=" "
          aria-invalid={error ? 'true' : 'false'}
          aria-describedby={error ? `${props.id}-error` : undefined}
          onFocus={() => setIsFocused(true)}
          onBlur={(e) => {
            setIsFocused(false);
            onBlur?.(e);
          }}
          onChange={handleChange}
          {...props}
        />
        {label && (
          <label htmlFor={props.id} className={`field-label ${isFloated ? 'field-label-floated' : ''}`}>
            {label}
            {required && <span className="required-mark" aria-hidden="true"> *</span>}
          </label>
        )}
        <button
          type="button"
          className="password-toggle"
          onClick={() => setShowPassword(!showPassword)}
          aria-label={showPassword ? 'Hide password' : 'Show password'}
          tabIndex={-1}
        >
          {showPassword ? (
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
              <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
              <line x1="1" y1="1" x2="23" y2="23"/>
            </svg>
          ) : (
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
              <circle cx="12" cy="12" r="3"/>
            </svg>
          )}
        </button>
      </div>

      {showStrength && value && (
        <div className="strength-indicator animate-slide-down">
          <div className="strength-bar">
            {[1, 2, 3, 4].map((level) => (
              <div
                key={level}
                className="strength-segment"
                style={{
                  backgroundColor: strength >= level ? STRENGTH_COLORS[strength] : 'var(--color-border)'
                }}
              />
            ))}
          </div>
          <span className="strength-label" style={{ color: STRENGTH_COLORS[strength] }}>
            {STRENGTH_LABELS[strength]}
          </span>
        </div>
      )}

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

PasswordInput.displayName = 'PasswordInput';

export default PasswordInput;
