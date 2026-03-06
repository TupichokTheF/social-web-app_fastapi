import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import AuthLayout from '../components/AuthLayout';
import InputField from '../components/InputField';
import PasswordInput from '../components/PasswordInput';
import Button from '../components/Button';
import SocialAuth from '../components/SocialAuth';
import Divider from '../components/Divider';
import { validateEmail } from '../utils/validation';
import { registerUser } from '../utils/api';
import './SignUpPage.css';

const containerVariants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.07, delayChildren: 0.1 }
  }
};

const itemVariants = {
  hidden: { opacity: 0, y: 10 },
  show: { opacity: 1, y: 0, transition: { duration: 0.4, ease: [0.22, 1, 0.36, 1] } }
};

const SignUpPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    agreeToTerms: false
  });
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [serverError, setServerError] = useState('');

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    const newValue = type === 'checkbox' ? checked : value;
    setFormData(prev => ({ ...prev, [name]: newValue }));
    if (errors[name]) setErrors(prev => ({ ...prev, [name]: '' }));
    if (serverError) setServerError('');
  };

  const validateField = (name, value) => {
    let error = '';
    switch (name) {
      case 'email':
        if (!value) error = 'Email is required';
        else if (!validateEmail(value)) error = 'Enter a valid email address';
        break;
      case 'password':
        if (!value) error = 'Password is required';
        else if (value.length < 8) error = 'At least 8 characters';
        break;
      case 'confirmPassword':
        if (!value) error = 'Please confirm your password';
        else if (value !== formData.password) error = 'Passwords do not match';
        break;
      case 'agreeToTerms':
        if (!value) error = 'You must accept the terms';
        break;
      default:
        break;
    }
    setErrors(prev => ({ ...prev, [name]: error }));
    return error;
  };

  const handleBlur = (e) => {
    const { name } = e.target;
    setTouched(prev => ({ ...prev, [name]: true }));
    validateField(name, formData[name]);
  };

  const validateForm = () => {
    const newErrors = {};
    Object.keys(formData).forEach(key => {
      const err = validateField(key, formData[key]);
      if (err) newErrors[key] = err;
    });
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setServerError('');
    const allTouched = Object.keys(formData).reduce((acc, key) => ({ ...acc, [key]: true }), {});
    setTouched(allTouched);
    if (!validateForm()) return;

    setIsLoading(true);
    try {
      const response = await registerUser({
        email: formData.email,
        password: formData.password
      });
      if (response.access_token) {
        localStorage.setItem('access_token', response.access_token);
        navigate('/dashboard');
      }
    } catch (error) {
      setServerError(error.message || 'Registration failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthLayout>
      <motion.div variants={containerVariants} initial="hidden" animate="show">
        <motion.div variants={itemVariants} className="auth-header">
          <h1 className="auth-title">Create account</h1>
          <p className="auth-subtitle">Start your journey with us</p>
        </motion.div>

        <motion.div variants={itemVariants}>
          <SocialAuth />
        </motion.div>

        <motion.div variants={itemVariants}>
          <Divider text="or" />
        </motion.div>

        <motion.form variants={itemVariants} onSubmit={handleSubmit} noValidate>
          {serverError && (
            <div className="server-error animate-slide-down" role="alert">
              {serverError}
            </div>
          )}

          <InputField
            id="email"
            name="email"
            type="email"
            label="Email"
            value={formData.email}
            onChange={handleChange}
            error={touched.email && errors.email}
            required
            autoComplete="email"
          />

          <PasswordInput
            id="password"
            name="password"
            label="Create a password"
            value={formData.password}
            onChange={handleChange}
            error={touched.password && errors.password}
            showStrength
            required
            autoComplete="new-password"
          />

          <PasswordInput
            id="confirmPassword"
            name="confirmPassword"
            label="Confirm password"
            value={formData.confirmPassword}
            onChange={handleChange}
            error={touched.confirmPassword && errors.confirmPassword}
            required
            autoComplete="new-password"
          />

          <div className="terms-field">
            <label className="terms-label">
              <input
                type="checkbox"
                name="agreeToTerms"
                checked={formData.agreeToTerms}
                onChange={handleChange}
                className="terms-checkbox"
              />
              <span>
                I agree to the{' '}
                <Link to="/terms" className="terms-link" target="_blank" rel="noopener noreferrer">
                  Terms of Service
                </Link>
                {' '}and{' '}
                <Link to="/privacy" className="terms-link" target="_blank" rel="noopener noreferrer">
                  Privacy Policy
                </Link>
              </span>
            </label>
            {touched.agreeToTerms && errors.agreeToTerms && (
              <span className="field-error-message animate-slide-down" role="alert">
                {errors.agreeToTerms}
              </span>
            )}
          </div>

          <Button
            type="submit"
            variant="primary"
            size="large"
            fullWidth
            loading={isLoading}
            disabled={isLoading}
          >
            Create account
          </Button>
        </motion.form>

        <motion.p variants={itemVariants} className="auth-switch">
          Already have an account?{' '}
          <Link to="/login" className="auth-link">
            Sign in
          </Link>
        </motion.p>
      </motion.div>
    </AuthLayout>
  );
};

export default SignUpPage;
