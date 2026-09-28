interface ProfileProps {
    username: string;
    email: string;
    photoUrl: string;
}

function Profile({ username, email, photoUrl }: ProfileProps) {
    return (
        <div className="profile">
            <img src={photoUrl} alt={username} />
            <h2>{username}</h2>
        </div>
    );
}

export default Profile;