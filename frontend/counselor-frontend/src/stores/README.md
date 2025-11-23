# Zustand Stores

This directory contains Zustand stores for global state management in the Gluide Counselor Frontend.

## Course Scheduler Store

The course scheduler store manages the state for the interactive course scheduling interface.

### Features

- **Term Management** - Manage multiple academic terms with courses
- **Course Placement** - Add, remove, and move courses between terms
- **Connections** - Track prerequisite and corequisite relationships
- **Undo/Redo** - Full undo/redo functionality for all changes
- **Search Filters** - Filter courses by query, department, credits
- **Persistence** - Automatically saves to localStorage
- **DevTools** - Redux DevTools integration for debugging

### Usage

```typescript
import { useCourseSchedulerStore } from '@/stores';

function CourseScheduler() {
  const {
    terms,
    connections,
    searchFilters,
    selectedCourseId,
    addCourseToTerm,
    removeCourseFromTerm,
    moveCourse,
    setSearchFilters,
    undo,
    redo,
    clearSchedule,
  } = useCourseSchedulerStore();

  // Add a course to a term
  const handleAddCourse = () => {
    addCourseToTerm(1, {
      id: 'cs101',
      course_code: 'CS101',
      course_name: 'Introduction to Computer Science',
      credits: 3,
      department: 'Computer Science',
    });
  };

  // Remove a course from a term
  const handleRemoveCourse = () => {
    removeCourseFromTerm(1, 'cs101');
  };

  // Move a course between terms
  const handleMoveCourse = () => {
    moveCourse(1, 2, 'cs101'); // Move from term 1 to term 2
  };

  // Update search filters
  const handleSearch = (query: string) => {
    setSearchFilters({ query });
  };

  return (
    <div>
      {/* Your scheduler UI */}
    </div>
  );
}
```

### State Structure

```typescript
interface CourseSchedulerState {
  // Current state
  terms: Term[];                    // Array of 4 terms with courses
  connections: Connection[];         // Prerequisite/corequisite connections
  searchFilters: SearchFilters;     // Active search filters
  selectedCourseId: string | null;  // Currently selected course
  isLoading: boolean;                // Loading state
  error: string | null;              // Error message

  // History for undo/redo
  undoStack: Term[][];              // Previous states
  redoStack: Term[][];              // Future states (after undo)
}
```

### Actions

**Term Actions:**
- `setTerms(terms: Term[])` - Replace all terms (adds to undo stack)
- `addCourseToTerm(termId: number, course: PlacedCourse)` - Add course to term
- `removeCourseFromTerm(termId: number, courseId: string)` - Remove course from term
- `moveCourse(fromTermId: number, toTermId: number, courseId: string)` - Move course

**Connection Actions:**
- `addConnection(connection: Connection)` - Add prerequisite/corequisite connection
- `removeConnection(connectionId: string)` - Remove connection

**Filter Actions:**
- `setSearchFilters(filters: Partial<SearchFilters>)` - Update search filters

**Selection Actions:**
- `setSelectedCourse(courseId: string | null)` - Select/deselect a course

**History Actions:**
- `undo()` - Undo last change
- `redo()` - Redo undone change

**Utility Actions:**
- `clearSchedule()` - Remove all courses from all terms
- `loadSchedule(scheduleData: Term[])` - Load saved schedule (resets undo/redo)

### Persistence

The store automatically persists to `localStorage` with the key `course-scheduler-storage`.

Only the following state is persisted:
- `terms` - All terms and their courses
- `connections` - All connections between courses

Other state (search filters, selection, undo/redo stacks) is not persisted.

### DevTools

Enable Redux DevTools in your browser to inspect state changes. The store is registered as `"CourseScheduler"`.

### Type Safety

All types are imported from `@/types/course-scheduler`:
- `Term` - Academic term with courses
- `PlacedCourse` - Course placed in a term
- `Connection` - Relationship between courses
- `SearchFilters` - Active search criteria

## Adding New Stores

1. Create a new file in this directory (e.g., `studentStore.ts`)
2. Define your state interface and actions
3. Create the store using Zustand
4. Export the store in `index.ts`

Example:

```typescript
// studentStore.ts
import { create } from "zustand";
import { devtools } from "zustand/middleware";

interface StudentState {
  students: Student[];
  setStudents: (students: Student[]) => void;
}

export const useStudentStore = create<StudentState>()(
  devtools(
    (set) => ({
      students: [],
      setStudents: (students) => set({ students }),
    }),
    { name: "Students" }
  )
);
```

```typescript
// index.ts
export { useCourseSchedulerStore } from './courseSchedulerStore';
export { useStudentStore } from './studentStore';
```
