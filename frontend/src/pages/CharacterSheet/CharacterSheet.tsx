import './characterSheet.css'
import { useState, useEffect, useRef } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import AbilityCard from '../../components/Ability/AbilityCard'
import ExitArrow from '../../assets/exitArrow.svg'
import Edit from '../../assets/edit.svg'
import Dice from '../../assets/dice.svg'
import Heart from '../../assets/heart.svg'
import Shield from '../../assets/shield.svg'
import Hexagon from '../../assets/hexagon.svg'
import Add from '../../assets/add.svg'
import Minus from '../../assets/minus.svg'
import ArrowLeft from '../../assets/arrow-left.svg'
import ArrowRight from '../../assets/arrow-right.svg'
import SanityBar from '../../assets/sanityBar.svg'
import Plus from '../../assets/plus.svg'

interface Attribute { id: number; name: string; value: number }
interface Skill { id: number; name: string; value: number }
interface Ability { id: number; name: string; description: string; image: string }

interface CharacterData {
    id: number;
    name: string;
    current_hp: number;
    max_hp: number;
    current_sanity: number;
    max_sanity: number;
    defense: number;
    image: string;
    notes: string;
    attributes: Attribute[];
    skills: Skill[];
    abilities: Ability[];
}

const authHeaders = () => ({
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('token')}`
});

const authHeadersFormData = () => ({
    'Authorization': `Bearer ${localStorage.getItem('token')}`
});

function CharacterSheet() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();

    const [character, setCharacter] = useState<CharacterData | null>(null);
    const [currentHp, setCurrentHp] = useState(0);
    const [currentSanity, setCurrentSanity] = useState(0);
    const [notes, setNotes] = useState('');
    const [loading, setLoading] = useState(true);
    const [isEditing, setIsEditing] = useState(false);

    useEffect(() => {
        fetch(`/characters/${id}`, { headers: authHeaders() })
            .then(res => { if (!res.ok) throw new Error("Erro ao carregar ficha"); return res.json(); })
            .then((data: CharacterData) => {
                setCharacter(data);
                setCurrentHp(data.current_hp);
                setCurrentSanity(data.current_sanity);
                setNotes(data.notes || '');
                setLoading(false);
            })
            .catch(err => {
                console.error(err);
                alert("Não foi possível carregar esta ficha.");
                navigate('/dashboard');
            });
    }, [id, navigate]);

    const getImageUrl = (path: string, type: 'abilities' | 'characters') => {
        if (!path) return '';
        if (path.startsWith('blob:') || path.startsWith('http')) return path;
        return `/${type}/uploads/${path}`;
    };

    const updateCharacter = (payload: Partial<CharacterData>, imageFile?: File) => {
        const formData = new FormData();
        Object.entries(payload).forEach(([key, value]) => {
            if (key === 'image') return;
            formData.append(key, String(value));
        });
        if (imageFile) formData.append('image', imageFile);

        fetch(`/characters/${id}`, {
            method: 'PUT',
            headers: authHeadersFormData(),
            body: formData
        }).catch(err => console.error("Erro ao salvar personagem:", err));
    };

    const handleHpChange = (amount: number) => {
        if (!character) return;
        const newHp = Math.min(character.max_hp, Math.max(0, currentHp + amount));
        setCurrentHp(newHp);
        updateCharacter({ current_hp: newHp });
    };
    const handleSanityChange = (amount: number) => {
        if (!character) return;
        const newSanity = Math.min(character.max_sanity, Math.max(0, currentSanity + amount));
        setCurrentSanity(newSanity);
        updateCharacter({ current_sanity: newSanity });
    };

    const notesTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
    const handleNotesChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        const value = e.target.value;
        setNotes(value);
        if (notesTimer.current) clearTimeout(notesTimer.current);
        notesTimer.current = setTimeout(() => updateCharacter({ notes: value }), 600);
    };

    const handleCharacterImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file || !character) return;
        const previewUrl = URL.createObjectURL(file);
        setCharacter({ ...character, image: previewUrl });
        updateCharacter({}, file);
    };

    const patchAttribute = (attrId: number, value: number) => {
        if (!character) return;
        setCharacter({
            ...character,
            attributes: character.attributes.map(a => a.id === attrId ? { ...a, value } : a)
        });
    };
    const patchSkill = (skillId: number, patch: Partial<Skill>) => {
        if (!character) return;
        setCharacter({
            ...character,
            skills: character.skills.map(s => s.id === skillId ? { ...s, ...patch } : s)
        });
    };
    const patchAbility = (abilityId: number, patch: Partial<Ability>) => {
        if (!character) return;
        setCharacter({
            ...character,
            abilities: character.abilities.map(a => a.id === abilityId ? { ...a, ...patch } : a)
        });
    };

    const saveAttribute = (attr: Attribute) =>
        fetch(`/attributes/${attr.id}`, {
            method: 'PUT', headers: authHeaders(), body: JSON.stringify({ value: attr.value })
        }).catch(err => console.error(err));

    const saveSkill = (skill: Skill) => {
        if (skill.id < 0) {
            fetch(`/skills`, {
                method: 'POST', headers: authHeaders(),
                body: JSON.stringify({ character_id: character!.id, name: skill.name, value: skill.value })
            })
            .then(r => r.json())
            .then((res: { id: number }) => {
                setCharacter(prev => prev ? {
                    ...prev,
                    skills: prev.skills.map(s => s.id === skill.id ? { ...s, id: res.id } : s)
                } : prev);
            }).catch(err => console.error(err));
        } else {
            fetch(`/skills/${skill.id}`, {
                method: 'PUT', headers: authHeaders(),
                body: JSON.stringify({ name: skill.name, value: skill.value })
            }).catch(err => console.error(err));
        }
    };

    const saveAbility = (ability: Ability, imageFile?: File) => {
        const formData = new FormData();
        formData.append('name', ability.name);
        formData.append('description', ability.description);
        if (imageFile) formData.append('image', imageFile);

        if (ability.id < 0) {
            formData.append('character_id', String(character!.id));
            fetch(`/abilities`, {
                method: 'POST',
                headers: authHeadersFormData(),
                body: formData
            })
            .then(r => r.json())
            .then((res: { id: number }) => {
                setCharacter(prev => prev ? {
                    ...prev,
                    abilities: prev.abilities.map(a => a.id === ability.id ? { ...a, id: res.id } : a)
                } : prev);
            }).catch(err => console.error(err));
        } else {
            fetch(`/abilities/${ability.id}`, {
                method: 'PUT',
                headers: authHeadersFormData(),
                body: formData
            }).catch(err => console.error(err));
        }
    };

    const handleAbilityImageChange = (ability: Ability, e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;
        const previewUrl = URL.createObjectURL(file);
        patchAbility(ability.id, { image: previewUrl });
        saveAbility({ ...ability, image: previewUrl }, file);
    };

    const tempIdRef = useRef(-1);
    const addSkill = () => {
        if (!character) return;
        const newSkill: Skill = { id: tempIdRef.current--, name: 'Perícia nova', value: 0 };
        setCharacter({ ...character, skills: [...character.skills, newSkill] });
        saveSkill(newSkill);
    };
    const addAbility = () => {
        if (!character) return;
        const newAbility: Ability = { id: tempIdRef.current--, name: 'Habilidade nova', description: '', image: '' };
        setCharacter({ ...character, abilities: [...character.abilities, newAbility] });
        saveAbility(newAbility);
    };

    if (loading || !character) {
        return <div className="loading-screen">Carregando Grimório / Ficha de Personagem...</div>;
    }

    return (
        <div className='CharacterSheet-container'>
            <div className='CharacterSheet-header'>
                <button onClick={() => navigate(-1)}><img src={ExitArrow} alt="botão de saída"/></button>
            </div>
            <div className='CharacterSheet-content'>
                <div className='CharacterSheet-character'>
                    <div className='edit-bottom'>
                        <button  className={isEditing ? 'edit-button active' : 'edit-button'} 
                        onClick={() => setIsEditing(prev => !prev)}>
                        <img src={Edit} alt="botão de edição"/>
                        </button>   
                    </div>
                    <h2>Ficha de personagem</h2>
                    <div className='CharacterSheet-profile'>
                        <div className='profile-image-wrapper'>
                            {isEditing ? (
                                <label htmlFor="character-image-input" className="character-image-label">
                                    <img
                                        className='Profile-img'
                                        src={character.image ? getImageUrl(character.image, 'characters') : "https://placehold.co/200x200"}
                                        alt="imagem do personagem"
                                    />
                                    <input
                                        id="character-image-input"
                                        type="file"
                                        accept="image/*"
                                        aria-label="imagem do personagem"
                                        onChange={handleCharacterImageChange}
                                        hidden
                                    />
                                </label>
                            ) : (
                                <img
                                    className='Profile-img'
                                    src={character.image ? getImageUrl(character.image, 'characters') : "https://placehold.co/200x200"}
                                    alt="imagem do personagem"
                                />
                            )}
                            <button className='dice-button'><img src={Dice} alt="botão de girar dados"/></button>
                            <div className='Shield'>
                                <img src={Shield} alt="defesa do personagem"/>
                                {isEditing ? (
                                    <input
                                        aria-label="defesa"
                                        type="number"
                                        value={character.defense}
                                        onChange={e => setCharacter({ ...character, defense: Number(e.target.value) })}
                                        onBlur={e => updateCharacter({ defense: Number(e.target.value) })}
                                    />
                                ) : (
                                    <p>{character.defense}</p>
                                )}
                            </div>
                            <div className='SanityBar'>
                                <img src={SanityBar} alt="barra de sanidade" className='sanityBar-img'/>
                                <div className='sanityBar-content'>
                                    <button onClick={() => handleSanityChange(1)}><img src={Add} alt="Aumentar"/></button>
                                    <p className='sanity-current'>{currentSanity}</p>
                                    <p className='sanity-divider'>/</p>
                                    {isEditing ? (
                                        <input
                                            aria-label="sanity"
                                            type="number"
                                            className='sanity-max'
                                            value={character.max_sanity}
                                            onChange={e => setCharacter({ ...character, max_sanity: Number(e.target.value) })}
                                            onBlur={e => updateCharacter({ max_sanity: Number(e.target.value) })}
                                        />
                                    ) : (
                                        <p className='sanity-max'>{character.max_sanity}</p>
                                    )}
                                    <button onClick={() => handleSanityChange(-1)}><img src={Minus} alt="Diminuir"/></button>
                                </div>
                            </div>
                        </div>

                        <div className='profile-info'>
                            {isEditing ? (
                                <input
                                    type="text"
                                    aria-label="nome do personagem"
                                    value={character.name}
                                    onChange={e => setCharacter({ ...character, name: e.target.value })}
                                    onBlur={e => updateCharacter({ name: e.target.value })}
                                />
                            ) : (
                                <h3>{character.name}</h3>
                            )}
                        </div>

                        <div className='lifeBar-container'>
                            <img src={Heart} alt="vida do personagem"/>
                            <div className='lifeBar'>
                                <button onClick={() => handleHpChange(-1)}><img src={ArrowLeft} alt="Diminuir"/></button>
                                {isEditing ? (
                                    <span>
                                        {currentHp} /{' '}
                                        <input
                                            aria-label="hp"
                                            type="number"
                                            value={character.max_hp}
                                            onChange={e => setCharacter({ ...character, max_hp: Number(e.target.value) })}
                                            onBlur={e => updateCharacter({ max_hp: Number(e.target.value) })}
                                        />
                                    </span>
                                ) : (
                                    <span>{currentHp} / {character.max_hp}</span>
                                )}
                                <button onClick={() => handleHpChange(1)}><img src={ArrowRight} alt="Aumentar"/></button>
                            </div>
                        </div>
                    </div>

                    {character.attributes.map(attr => (
                        <div className='CharacterSheet-attributes' key={attr.id}>
                            <div className='attribute-icon'>
                                <img src={Hexagon} alt="hexágono de atributo"/>
                                {isEditing ? (
                                    <input
                                        aria-label="attribute"
                                        type="number"
                                        value={attr.value}
                                        onChange={e => patchAttribute(attr.id, Number(e.target.value))}
                                        onBlur={() => saveAttribute(attr)}
                                    />
                                ) : (
                                    <p>{attr.value}</p>
                                )}
                            </div>
                            <h2>{attr.name}</h2>
                        </div>
                    ))}
                </div>

                <div className='CharacterSheet-skill'>
                    <div className='section-header'>
                        {isEditing && <span className='header-spacer' />}
                        <h2>Perícias</h2>
                        {isEditing && (
                            <button className='add-button' onClick={addSkill}>
                                <img src={Plus} alt="Adicionar perícia"/>
                            </button>
                        )}
                    </div>   
                    <ol>
                        {character.skills.map(skill => (
                            <li key={skill.id}>
                                {isEditing ? (
                                    <input
                                        type="text"
                                        aria-label={`nome de ${skill.name}`}
                                        value={skill.name}
                                        onChange={e => patchSkill(skill.id, { name: e.target.value })}
                                        onBlur={() => saveSkill(skill)}
                                    />
                                ) : (
                                    <p>{skill.name}</p>
                                )}
                                <input
                                    type="number"
                                    aria-label={skill.name}
                                    value={skill.value}
                                    readOnly={!isEditing}
                                    onChange={e => patchSkill(skill.id, { value: Number(e.target.value) })}
                                    onBlur={() => saveSkill(skill)}
                                />
                            </li>
                        ))}
                    </ol>
                </div>

                <div className='CharacterSheet-abilities-inventory'>
                    <div className='section-header'>
                        {isEditing && <span className='header-spacer' />}
                        <h2>Habilidades</h2>
                        {isEditing && (
                            <button className='add-button' onClick={addAbility}>
                                <img src={Plus} alt="Adicionar habilidade"/>
                            </button>
                        )}
                    </div>
                    <ol>
                        {character.abilities.map(ability => (
                            isEditing ? (
                                <li key={ability.id} className='AbilityCard-container ability-edit-item'>
                                    <label htmlFor={`ability-image-${ability.id}`} className="ability-image-label">
                                        <img
                                            src={ability.image ? getImageUrl(ability.image, 'abilities') : "https://placehold.co/50x50"}
                                            alt="Imagem da habilidade"
                                        />
                                        <input
                                            id={`ability-image-${ability.id}`}
                                            type="file"
                                            accept='image/*'
                                            aria-label="imagem"
                                            onChange={e => handleAbilityImageChange(ability, e)}
                                            hidden
                                        />
                                    </label>
                                    <div className='AbilityCard-text'>
                                        <input
                                            type="text"
                                            className='ability-name-input'
                                            aria-label="nome da habilidade"
                                            value={ability.name}
                                            onChange={e => patchAbility(ability.id, { name: e.target.value })}
                                            onBlur={() => saveAbility(ability)}
                                        />
                                        <textarea className='ability-description'
                                            aria-label="descrição da habilidade"
                                            value={ability.description}
                                            onChange={e => patchAbility(ability.id, { description: e.target.value })}
                                            onBlur={() => saveAbility(ability)}
                                        />
                                    </div>
                                </li>
                            ) : (
                                <AbilityCard
                                    title={ability.name}
                                    description={ability.description}
                                    image={ability.image ? getImageUrl(ability.image, 'abilities') : "https://placehold.co/50x50"}
                                    key={ability.id}
                                />
                            )
                        ))}
                    </ol>
                    <h2>Anotações</h2>
                    <textarea
                        aria-label="anotações"
                        name="anotações"
                        id="inventory"
                        value={notes}
                        onChange={handleNotesChange}
                    ></textarea>
                </div>
            </div>
        </div>
    )
}

export default CharacterSheet;