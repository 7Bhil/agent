# Cadre Visuel & Système de Design UI (DESIGN-SYSTEM.md)

Ce document établit la direction artistique, la palette sémantique, la typographie et les états d'interface obligatoires du projet. Il sert de source unique de vérité visuelle pour l'équipe et les agents d'ingénierie front-end.

---

## 1. Principes Visuels Fondamentaux
- **Sobriété d'Entreprise** : Interfaces nettes, lisibles, professionnelles et axées sur l'efficacité métier.
- **Interdiction Formelle des Styles IA Stéréotypés** :
  - Zéro dégradé fluo (violet/indigo arbitraire non justifié).
  - Zéro glassmorphism kitsch ou cartes lumineuses non demandées.
  - Zéro couleur brute injectée en dur (`#hex`, `rgb(...)`) dans les balises JSX ou HTML.
- **Accessibilité Native (WCAG 2.2 AA)** :
  - Ratio de contraste minimal de 4.5:1 pour le texte standard et 3:1 pour le texte large et les éléments interactifs.
  - Indicateur de focus visible sur chaque composant interactif (`focus-visible:ring-2 focus-visible:ring-primary`).

---

## 2. Palette Sémantique et Tokens (Tailwind / CSS Variables)

Toute couleur utilisée dans l'interface doit correspondre à l'un des rôles sémantiques ci-dessous :

```css
:root {
  /* Arrière-plans et Surfaces */
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --card: 0 0% 100%;
  --card-foreground: 222.2 84% 4.9%;

  /* Actions Principales & Accents */
  --primary: 221.2 83.2% 53.3%;
  --primary-foreground: 210 40% 98%;
  --secondary: 210 40% 96.1%;
  --secondary-foreground: 222.2 47.4% 11.2%;

  /* Éléments Neutres et Bordures */
  --muted: 210 40% 96.1%;
  --muted-foreground: 215.4 16.3% 46.9%;
  --border: 214.3 31.8% 91.4%;
  --input: 214.3 31.8% 91.4%;

  /* Feedback & Statuts Métier */
  --destructive: 0 84.2% 60.2%;
  --destructive-foreground: 210 40% 98%;
  --success: 142.1 76.2% 36.3%;
  --success-foreground: 355.7 100% 97.3%;
  --warning: 38 92% 50%;
  --warning-foreground: 48 96% 89%;
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  --card: 222.2 84% 4.9%;
  --card-foreground: 210 40% 98%;
  --primary: 217.2 91.2% 59.8%;
  --primary-foreground: 222.2 47.4% 11.2%;
  --secondary: 217.2 32.6% 17.5%;
  --secondary-foreground: 210 40% 98%;
  --muted: 217.2 32.6% 17.5%;
  --muted-foreground: 215 20.2% 65.1%;
  --border: 217.2 32.6% 17.5%;
  --input: 217.2 32.6% 17.5%;
}
```

---

## 3. Typographie & Rythme Visuel
- **Police Principale** : Sans-serif système propre et neutre (`Inter`, `system-ui`, `-apple-system`).
- **Échelle Typographique** :
  - Titre de page (`H1`) : `text-2xl font-bold tracking-tight` (desktop: `text-3xl`).
  - Titre de section (`H2`) : `text-xl font-semibold tracking-tight`.
  - Sous-titre (`H3`) : `text-lg font-medium`.
  - Corps de texte (`Body`) : `text-sm font-normal text-muted-foreground` ou `text-foreground`.
  - Données techniques / codes : `font-mono text-xs`.
- **Échelle d'Espacement & Grille** :
  - Espacement horizontal/vertical standardisé : multiples de 4px (`p-2`, `p-4`, `gap-4`, `space-y-6`).
  - Largeur de conteneur maximale : `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`.

---

## 4. Les 4 États Obligatoires de Chaque Composant

Tout composant affichant des données dynamiques doit implémenter formellement les 4 états suivants :

```
[Requête Déclenchée] ---> [1. Loading / Squelette]
                                |
          +---------------------+---------------------+
          |                                           |
          v                                           v
[2. Nominal / Données]                 [3. Empty / Liste Vide]
          |                                           |
          +---------------------+---------------------+
                                |
                                v (En cas d'échec)
                       [4. Error / Réessai]
```

1. **État de Chargement (`Loading`)** :
   - Préférer les squelettes animés (`Skeleton`) plutôt que les spinners bloquants plein écran.
   - Préserver la disposition spatiale pour éviter les sauts de contenu (*Cumulative Layout Shift - CLS*).
2. **État Vide (`Empty State`)** :
   - Message explicite expliquant l'absence d'éléments.
   - Bouton d'action contextuel clair (ex: *Créer une transaction*, *Inviter un collaborateur*).
3. **État d'Erreur (`Error State`)** :
   - Message d'erreur compréhensible par l'utilisateur (sans stack trace ni jargon technique interne).
   - Possibilité de réessai immédiat (*Bouton Réessayer*) ou guidage vers le support.
4. **État Nominal (`Data Loaded`)** :
   - Affichage complet, gestion fluide du dépassement de texte (`truncate`, infobulles).

---

## 5. Primitifs Recommandés & Écosystème
- **Composants d'Interface Non Stylés** : Radix UI / Headless UI pour garantir l'accessibilité native (gestion focus, attributs ARIA, navigation clavier).
- **Implémentation Modulaire** : Composants basés sur `shadcn/ui` intégrés directement dans le code source du projet pour conserver la maîtrise complète du code.
- **Gestion des Classes** : Utiliser la combinaison utilitaire `clsx` et `tailwind-merge` (`cn(...)`) pour éviter les conflits de classes CSS.
