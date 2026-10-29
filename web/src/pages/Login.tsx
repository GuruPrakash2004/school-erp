import { useState, type FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { api, TOKEN_KEY } from '../api'

export default function Login() {
  const navigate = useNavigate()
  const [schoolId, setSchoolId] = useState('1')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    try {
      const res = await api.post<{ access_token: string }>('/auth/login', {
        school_id: Number(schoolId),
        email,
        password,
      })
      localStorage.setItem(TOKEN_KEY, res.data.access_token)
      navigate('/marks')
    } catch (err) {
      if (axios.isAxiosError(err) && err.response) {
        const detail = err.response.data?.detail
        setError(typeof detail === 'string' ? detail : 'Login failed')
      } else {
        setError('Cannot reach the server')
      }
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h1>Login</h1>
      <div>
        <label>
          School ID{' '}
          <input value={schoolId} onChange={(e) => setSchoolId(e.target.value)} required />
        </label>
      </div>
      <div>
        <label>
          Email{' '}
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
      </div>
      <div>
        <label>
          Password{' '}
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
      </div>
      <button type="submit">Log in</button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </form>
  )
}
