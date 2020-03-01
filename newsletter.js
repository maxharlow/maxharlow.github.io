document.querySelector('form').addEventListener('submit', async event => {
    event.preventDefault()
    if (document.querySelector('form button').disabled) return
    document.querySelector('form button').setAttribute('disabled', '')
    document.querySelector('form span').innerHTML = 'Loading...'
    const email = document.querySelector('form input').value
    try {
        if (!email) throw new Error()
        await fetch('https://buttondown.email/api/emails/subscribers/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            referrer: '',
            body: JSON.stringify({ email, newsletter: 'b11d23c6-9710-4496-85c9-0c156550f0de' })
        })
        document.querySelector('form span').innerHTML = 'Thanks for subscribing! Please check your email to confirm.'
    }
    catch (e) {
        document.querySelector('form span').innerHTML = 'There was an error. Please check your email is correct and try again.'
        console.error(e)
    }
    finally {
        document.querySelector('form button').removeAttribute('disabled')
    }
})
