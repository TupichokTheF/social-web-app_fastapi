import './Divider.css';

const Divider = ({ text = 'или' }) => {
  return (
    <div className="divider">
      <span className="divider-line"></span>
      <span className="divider-text">{text}</span>
      <span className="divider-line"></span>
    </div>
  );
};

export default Divider;
