import { type Environment } from '~/api/client'
import useLocalStorage from '~/hooks/useLocalStorage'
import { isArrayEmpty, isFalse, isStringEmptyOrNil } from '~/utils'

export const EnumDefaultEnvironment = {
  Empty: '',
  Prod: 'prod',
} as const

export const EnumRelativeLocation = {
  Local: 'local',
  Syncronized: 'syncronized',
} as const

export type EnvironmentName = DefaultEnvironment | string
export type DefaultEnvironment = KeyOf<typeof EnumDefaultEnvironment>
export type RelativeLocation = KeyOf<typeof EnumRelativeLocation>

interface InitialEnvironmemt extends Partial<Environment> {
  name: EnvironmentName
}

interface ProfileEnvironment {
  name: EnvironmentName
  createFrom: EnvironmentName
}

interface Profile {
  environment: ProfileEnvironment
  environments: ProfileEnvironment[]
}

const [getProfile, setProfile] = useLocalStorage<Profile>('profile')

export class ModelEnvironment {
  private _initial: InitialEnvironmemt
  private _type: RelativeLocation
  private _createFrom: EnvironmentName

  isModel = true

  constructor(
    initial: InitialEnvironmemt,
    type: RelativeLocation,
    createFrom: EnvironmentName = EnumDefaultEnvironment.Prod,
  ) {
    this._initial = initial
    this._type = type ?? EnumRelativeLocation.Local
    this._createFrom = this.isDefault
      ? EnumDefaultEnvironment.Empty
      : createFrom
  }

  get name(): string {
    return this._initial.name
  }

  get type(): string {
    return this._type
  }

  get createFrom(): string {
    return this._createFrom
  }

  get isDefault(): boolean {
    return this.name === EnumDefaultEnvironment.Prod
  }

  get isInitial(): boolean {
    return isStringEmptyOrNil(this._initial.plan_id)
  }

  get isLocal(): boolean {
    return this._type === EnumRelativeLocation.Local
  }

  get isSyncronized(): boolean {
    return this._type === EnumRelativeLocation.Syncronized
  }

  setType(type: RelativeLocation): void {
    this._type = type
  }

  setCreatedFrom(createFrom: EnvironmentName): void {
    this._createFrom = createFrom
  }

  update(initial: InitialEnvironmemt): void {
    this._initial = initial
  }

  static save({
    environment,
    environments,
  }: {
    environment?: ModelEnvironment
    environments?: ModelEnvironment[]
  }): void {
    const output: Partial<Profile> = {}

    if (environment != null) {
      output.environment = {
        name: environment.name,
        createFrom: environment.createFrom,
      }
    }

    if (environments != null) {
      output.environments = ModelEnvironment.getOnlyLocal(environments).map(
        env => ({
          name: env.name,
          createFrom: env.createFrom,
        }),
      )
    }

    setProfile(output)
  }

  static getOnlyLocal(envs: ModelEnvironment[] = []): ModelEnvironment[] {
    return envs.filter(
      env => isFalse(isStringEmptyOrNil(env.name)) && env.isLocal,
    )
  }

  static getOnlySyncronized(envs: ModelEnvironment[] = []): ModelEnvironment[] {
    return envs.filter(
      env => isFalse(isStringEmptyOrNil(env.name)) && env.isSyncronized,
    )
  }

  static getDefaultEnvironments(): ModelEnvironment[] {
    const profile = getProfile()
    const environments = new Map<EnvironmentName, ProfileEnvironment>()

    if (profile?.environment != null) {
      environments.set(profile.environment.name, profile.environment)
    }

    if (profile?.environments != null) {
      profile.environments.forEach(environment =>
        environments.set(environment.name, environment),
      )
    }

    const output: ModelEnvironment[] = []

    Array.from(environments.entries()).forEach(([name, environment]) => {
      output.push(
        new ModelEnvironment(
          { name },
          EnumRelativeLocation.Local,
          environment.createFrom,
        ),
      )
    })

    if (isArrayEmpty(output)) {
      output.push(
        new ModelEnvironment(
          { name: EnumDefaultEnvironment.Prod },
          EnumRelativeLocation.Local,
        ),
      )
    }

    return output
  }

  static sort(environments: ModelEnvironment[]): ModelEnvironment[] {
    environments.sort(env => (env.isSyncronized ? -1 : 1))

    return environments
  }
}
