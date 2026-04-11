import { useAuth0 } from '@auth0/auth0-react'
import './App.css'

function App() {
  const {
    isLoading,
    isAuthenticated,
    error,
    loginWithRedirect,
    logout,
    user,
  } = useAuth0()

  const signup = () =>
    loginWithRedirect({
      authorizationParams: { screen_hint: 'signup' },
    })

  if (isLoading) return <h2>Loading...</h2>

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial, sans-serif' }}>
      <h1>MLH API Assistant</h1>
      <p>Initial Auth0 login flow for MLH API Week.</p>

      {isAuthenticated ? (
        <>
          <p>Logged in as: {user?.email}</p>
          <pre>{JSON.stringify(user, null, 2)}</pre>
          <button
            onClick={() =>
              logout({ logoutParams: { returnTo: window.location.origin } })
            }
          >
            Logout
          </button>
        </>
      ) : (
        <>
          {error && <p>Error: {error.message}</p>}
          <button onClick={signup}>Sign up</button>
          <button onClick={() => loginWithRedirect()} style={{ marginLeft: '1rem' }}>
            Login
          </button>
        </>
      )}
    </div>
  )
}

export default App