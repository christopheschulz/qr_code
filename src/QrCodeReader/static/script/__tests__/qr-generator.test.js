/**
 * @jest-environment jsdom
 */

const { containsInvalidChars, escapeHtml } = require('../qr-generator');

// ============================================================
// containsInvalidChars - Détection des caractères hors Latin-1
// ============================================================

describe('containsInvalidChars', () => {

    // --- Caractères VALIDES (Latin-1 / ISO 8859-1) ---

    test('accepte une chaîne ASCII simple', () => {
        expect(containsInvalidChars('Hello world')).toBe(false);
    });

    test('accepte une chaîne vide', () => {
        expect(containsInvalidChars('')).toBe(false);
    });

    test('accepte les chiffres et la ponctuation', () => {
        expect(containsInvalidChars('12345 !@#$%^&*()_+-=[]{}|;:,.<>?')).toBe(false);
    });

    test('accepte les accents français (é, è, ê, à, ç, ü)', () => {
        expect(containsInvalidChars('Café résumé naïve àéîõü')).toBe(false);
    });

    test('accepte les caractères espagnols (ñ, ¿, ¡)', () => {
        expect(containsInvalidChars('¿Hola? Ñoño ¡Sí!')).toBe(false);
    });

    test('accepte les caractères allemands (ö, ä, ü, ß)', () => {
        expect(containsInvalidChars('über Straße Mädchen')).toBe(false);
    });

    test('accepte les symboles Latin-1 (©, ®, £, ¥, §)', () => {
        expect(containsInvalidChars('©2024 ®marque £50 ¥100 §1')).toBe(false);
    });

    test('accepte les caractères de contrôle (retour ligne, tabulation)', () => {
        expect(containsInvalidChars('ligne1\nligne2\tcolonne')).toBe(false);
    });

    test('accepte une URL standard', () => {
        expect(containsInvalidChars('https://example.com/page?id=123&lang=fr')).toBe(false);
    });

    test('accepte un format vCard', () => {
        expect(containsInvalidChars('BEGIN:VCARD\nVERSION:3.0\nFN:René Müller\nEND:VCARD')).toBe(false);
    });

    test('accepte un format WiFi', () => {
        expect(containsInvalidChars('WIFI:T:WPA;S:MonRéseau;P:motdepàsse;;')).toBe(false);
    });

    // --- Caractères INVALIDES (hors Latin-1) ---

    test('rejette un emoji simple (😀)', () => {
        expect(containsInvalidChars('Hello 😀')).toBe(true);
    });

    test('rejette les emojis variés (🎉🔥👍)', () => {
        expect(containsInvalidChars('Test 🎉🔥👍')).toBe(true);
    });

    test('rejette un emoji seul', () => {
        expect(containsInvalidChars('🎉')).toBe(true);
    });

    test('rejette les caractères chinois', () => {
        expect(containsInvalidChars('Hello 你好世界')).toBe(true);
    });

    test('rejette les caractères arabes', () => {
        expect(containsInvalidChars('Bienvenue مرحبا')).toBe(true);
    });

    test('rejette les caractères japonais (hiragana)', () => {
        expect(containsInvalidChars('こんにちは')).toBe(true);
    });

    test('rejette les caractères coréens', () => {
        expect(containsInvalidChars('안녕하세요')).toBe(true);
    });

    test('rejette les caractères cyrilliques', () => {
        expect(containsInvalidChars('Привет мир')).toBe(true);
    });

    test('rejette le symbole téléphone emoji (☎️)', () => {
        // ☎ est U+260E (> 0xFF)
        expect(containsInvalidChars('Contact: ☎')).toBe(true);
    });

    test('rejette un emoji caché au milieu du texte', () => {
        expect(containsInvalidChars('texte normal 💡 suite du texte')).toBe(true);
    });

    test('rejette les flèches Unicode hors Latin-1 (→)', () => {
        // → est U+2192 (> 0xFF)
        expect(containsInvalidChars('cliquez → ici')).toBe(true);
    });
});

// ============================================================
// escapeHtml - Protection contre l'injection XSS
// ============================================================

describe('escapeHtml', () => {

    test('retourne le texte tel quel sans caractères spéciaux', () => {
        expect(escapeHtml('Bonjour monde')).toBe('Bonjour monde');
    });

    test('échappe les chevrons < et >', () => {
        expect(escapeHtml('<script>alert("xss")</script>')).toBe(
            '&lt;script&gt;alert("xss")&lt;/script&gt;'
        );
    });

    test('échappe les guillemets doubles', () => {
        expect(escapeHtml('valeur="test"')).toBe('valeur="test"');
        // Note: textContent/innerHTML ne transforme pas les guillemets doubles
        // sauf dans un contexte d'attribut
    });

    test('échappe le &', () => {
        expect(escapeHtml('A & B')).toBe('A &amp; B');
    });

    test('gère une chaîne vide', () => {
        expect(escapeHtml('')).toBe('');
    });

    test('échappe une balise HTML complète', () => {
        const input = '<img src=x onerror=alert(1)>';
        const result = escapeHtml(input);
        expect(result).not.toContain('<img');
        expect(result).toContain('&lt;');
    });

    test('préserve les accents et caractères spéciaux Latin-1', () => {
        expect(escapeHtml('Café © Ñoño')).toBe('Café © Ñoño');
    });
});
