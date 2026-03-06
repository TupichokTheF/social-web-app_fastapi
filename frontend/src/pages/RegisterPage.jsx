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
import './RegisterPage.css';

const RegisterPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
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

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
    if (serverError) {
      setServerError('');
    }
  };

  const handleBlur = (e) => {
    const { name } = e.target;
    setTouched(prev => ({ ...prev, [name]: true }));
    validateField(name, formData[name]);
  };

  const validateField = (name, value) => {
    let error = '';

    switch (name) {
      case 'name':
        if (!value) {
          error = 'Имя обязательно';
        } else if (value.length < 2) {
          error = 'Минимум 2 символа';
        }
        break;
      case 'email':
        if (!value) {
          error = 'Email обязателен';
        } else if (!validateEmail(value)) {
          error = 'Введите корректный email';
        }
        break;
      case 'password':
        if (!value) {
          error = 'Пароль обязателен';
        } else if (value.length < 8) {
          error = 'Минимум 8 символов';
        }
        // Revalidate confirmPassword if it was already touched
        if (touched.confirmPassword && formData.confirmPassword) {
          validateField('confirmPassword', formData.confirmPassword);
        }
        break;
      case 'confirmPassword':
        if (!value) {
          error = 'Подтвердите пароль';
        } else if (value !== formData.password) {
          error = 'Пароли не совпадают';
        }
        break;
      case 'agreeToTerms':
        if (!value) {
          error = 'Необходимо согласие';
        }
        break;
      default:
        break;
    }

    setErrors(prev => ({ ...prev, [name]: error }));
    return error;
  };

  const validateForm = () => {
    const newErrors = {};
    Object.keys(formData).forEach(key => {
      const error = validateField(key, formData[key]);
      if (error) newErrors[key] = error;
    });
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setServerError('');

    // Mark all fields as touched
    const allTouched = Object.keys(formData).reduce((acc, key) => {
      acc[key] = true;
      return acc;
    }, {});
    setTouched(allTouched);

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      const response = await registerUser({
        name: formData.name,
        email: formData.email,
        password: formData.password
      });

      // Save token to localStorage (refresh_token в httpOnly cookie на backend)
      if (response.access_token) {
        localStorage.setItem('access_token', response.access_token);
        navigate('/dashboard');
      }
    } catch (error) {
      setServerError(error.message || 'Ошибка регистрации. Попробуйте снова.');
    } finally {
      setIsLoading(false);
    }
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.08
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 12 },
    show: { opacity: 1, y: 0 }
  };

  return (
    <AuthLayout>
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="show"
      >
        <motion.div variants={itemVariants} className="auth-header">
          <h1 className="auth-title">Регистрация</h1>
          <p className="auth-subtitle">Создайте аккаунт, чтобы начать</p>
        </motion.div>

        <motion.div variants={itemVariants}>
          <SocialAuth />
        </motion.div>

        <motion.div variants={itemVariants}>
          <Divider />
        </motion.div>

        <motion.form variants={itemVariants} onSubmit={handleSubmit} noValidate>
          {serverError && (
            <div className="form-error animate-slide-down" role="alert">
              {serverError}
            </div>
          )}

          <InputField
            id="name"
            name="name"
            type="text"
            label="Имя"
            placeholder="Ваше имя"
            value={formData.name}
            onChange={handleChange}
            onBlur={handleBlur}
            error={touched.name && errors.name}
            required
            autoComplete="name"
          />

          <InputField
            id="email"
            name="email"
            type="email"
            label="Email"
            placeholder="your@email.com"
            value={formData.email}
            onChange={handleChange}
            onBlur={handleBlur}
            error={touched.email && errors.email}
            required
            autoComplete="email"
          />

          <PasswordInput
            id="password"
            name="password"
            label="Пароль"
            placeholder="Минимум 8 символов"
            value={formData.password}
            onChange={handleChange}
            onBlur={handleBlur}
            error={touched.password && errors.password}
            showStrength={true}
            required
            autoComplete="new-password"
          />

          <PasswordInput
            id="confirmPassword"
            name="confirmPassword"
            label="Подтвердите пароль"
            placeholder="Повторите пароль"
            value={formData.confirmPassword}
            onChange={handleChange}
            onBlur={handleBlur}
            error={touched.confirmPassword && errors.confirmPassword}
            required
            autoComplete="new-password"
          />

          <div className="checkbox-field">
            <input
              type="checkbox"
              id="agreeToTerms"
              name="agreeToTerms"
              checked={formData.agreeToTerms}
              onChange={handleChange}
              onBlur={handleBlur}
              className="checkbox"
              aria-describedby={touched.agreeToTerms && errors.agreeToTerms ? 'terms-error' : undefined}
            />
            <label htmlFor="agreeToTerms" className="checkbox-label">
              Я согласен с{' '}
              <Link to="/terms" className="terms-link" target="_blank">
                условиями использования
              </Link>
              {' '}и{' '}
              <Link to="/privacy" className="terms-link" target="_blank">
                политикой конфиденциальности
              </Link>
            </label>
          </div>
          {touched.agreeToTerms && errors.agreeToTerms && (
            <span id="terms-error" className="input-error-message animate-slide-down" role="alert">
              {errors.agreeToTerms}
            </span>
          )}

          <Button
            type="submit"
            variant="primary"
            size="large"
            fullWidth
            loading={isLoading}
            disabled={isLoading}
          >
            Зарегистрироваться
          </Button>

          <p className="auth-switch">
            Уже есть аккаунт?{' '}
            <Link to="/login" className="auth-link">
              Войти
            </Link>
          </p>
        </motion.form>
      </motion.div>
    </AuthLayout>
  );
};

export default RegisterPage;
