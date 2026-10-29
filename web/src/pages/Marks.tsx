import { useState, type FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { api, TOKEN_KEY } from '../api'

type Mark = { subject: string; exam_name: string; score: number }
type StudentMarks = { student_id: number; student_name: string; marks: Mark[] }

export default function Marks() {
  const navigate = useNavigate()
  const [studentId, setStudentId] = useState('')
  const [data, setData] = useState<StudentMarks | null>(null)
  const [error, setError] = useState('')

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    setData(null)
    try {
      const res = await api.get<StudentMarks>(`/students/${studentId}/marks`)
      setData(res.data)
    } catch (err) {
      if (axios.isAxiosError(err) && err.response) {
        const status = err.response.status
        if (status === 401) {
          localStorage.removeItem(TOKEN_KEY)
          navigate('/login')
        } else if (status === 403) {
          setError('Not allowed')
        } else if (status === 404) {
          setError('Student not found')
        } else {
          setError('Something went wrong')
        }
      } else {
        setError('Cannot reach the server')
      }
    }
  }

  function logout() {
    localStorage.removeItem(TOKEN_KEY)
    navigate('/login')
  }

  return (
    <div>
      <h1>Student marks</h1>
      <button onClick={logout}>Log out</button>
      <form onSubmit={handleSubmit}>
        <label>
          Student ID{' '}
          <input
            type="number"
            min="1"
            value={studentId}
            onChange={(e) => setStudentId(e.target.value)}
            required
          />
        </label>{' '}
        <button type="submit">Show marks</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {data && (
        <>
          <h2>{data.student_name}</h2>
          <table border={1} cellPadding={6}>
            <thead>
              <tr>
                <th>Subject</th>
                <th>Exam</th>
                <th>Score</th>
              </tr>
            </thead>
            <tbody>
              {data.marks.map((m) => (
                <tr key={`${m.subject}-${m.exam_name}`}>
                  <td>{m.subject}</td>
                  <td>{m.exam_name}</td>
                  <td>{m.score}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </div>
  )
}
